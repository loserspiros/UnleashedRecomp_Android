#define DOCTEST_CONFIG_IMPLEMENT_WITH_MAIN
#include "doctest.h"
#include <chrono>
#include <vector>
#include <unordered_map>
#include <string>
#include <iostream>

#pragma pack(push, 1)

// Definitions from xcontent_file_system.h/cpp
struct StfsDirectoryEntry
{
    char name[40];
    struct Flags
    {
        uint8_t nameLength : 6;
        uint8_t directory : 1;
        uint8_t unk : 1;
    } flags;
    uint8_t allocatedDataBlocksRaw[3];
    uint8_t unk1[2];
    uint8_t startBlockNumberRaw[3];
    uint16_t directoryIndex;
    uint32_t length;
    uint32_t creationDate;
    uint32_t updateDate;
};

struct StfsDirectoryBlock
{
    StfsDirectoryEntry entries[64];
};
#pragma pack(pop)

const uint32_t StfsEntriesPerDirectoryBlock = 64;
const uint32_t StfsEndOfChain = 0xFFFFFF;

struct FileInfo {
    uint32_t length;
    uint32_t blockIndex;
    uint32_t blockCount;
};

void parse_original(const uint8_t* rootMappedFileData, size_t baseOffset, uint32_t tableBlockCount, uint32_t initialTableBlockIndex, size_t rootMappedFileSize) {
    uint32_t entryCount = 0;
    uint32_t tableBlockIndex = initialTableBlockIndex;
    std::vector<std::string> directoryPaths;
    std::vector<uint32_t> entryToPathIndex(0x10000, 0xFFFFFFFF);
    // Dummy map for fileMap
    std::unordered_map<std::string, FileInfo> fileMap;
    fileMap.reserve(10000);

    for (uint32_t i = 0; i < tableBlockCount; i++)
    {
        size_t offset = tableBlockIndex * sizeof(StfsDirectoryBlock); // simplified offset
        if (offset + sizeof(StfsDirectoryBlock) > rootMappedFileSize)
        {
            return;
        }

        StfsDirectoryBlock *directoryBlock = (StfsDirectoryBlock *)(&rootMappedFileData[offset]);
        for (uint32_t j = 0; j < StfsEntriesPerDirectoryBlock; j++)
        {
            const StfsDirectoryEntry &directoryEntry = directoryBlock->entries[j];
            if (directoryEntry.name[0] == '\0')
            {
                break;
            }

            std::string fileNameBase;
            uint32_t pathIndex = entryToPathIndex[directoryEntry.directoryIndex];
            if (pathIndex != 0xFFFFFFFF)
            {
                fileNameBase = directoryPaths[pathIndex];
            }

            std::string fileName(directoryEntry.name, directoryEntry.flags.nameLength & 0x3F);
            if (directoryEntry.flags.directory)
            {
                if (entryCount < 0x10000)
                {
                    directoryPaths.push_back(fileNameBase + fileName + "/");
                    entryToPathIndex[entryCount] = (uint32_t)(directoryPaths.size() - 1);
                }
                entryCount++;
                continue;
            }

            uint32_t fileBlockIndex = 0; // dummy
            uint32_t fileBlockCount = 0; // dummy
            fileMap[fileNameBase + fileName] = { directoryEntry.length, fileBlockIndex, fileBlockCount };
            entryCount++;
        }
        tableBlockIndex++; // simplified iteration
    }
}

void parse_optimized(const uint8_t* rootMappedFileData, size_t baseOffset, uint32_t tableBlockCount, uint32_t initialTableBlockIndex, size_t rootMappedFileSize) {
    uint32_t entryCount = 0;
    uint32_t tableBlockIndex = initialTableBlockIndex;
    std::vector<std::string> directoryPaths;
    std::vector<uint32_t> entryToPathIndex(0x10000, 0xFFFFFFFF);
    // Dummy map for fileMap
    std::unordered_map<std::string, FileInfo> fileMap;
    fileMap.reserve(10000);

    for (uint32_t i = 0; i < tableBlockCount; i++)
    {
        size_t offset = tableBlockIndex * sizeof(StfsDirectoryBlock); // simplified offset
        if (offset + sizeof(StfsDirectoryBlock) > rootMappedFileSize)
        {
            return;
        }

        StfsDirectoryBlock *directoryBlock = (StfsDirectoryBlock *)(&rootMappedFileData[offset]);
        for (uint32_t j = 0; j < StfsEntriesPerDirectoryBlock; j++)
        {
            const StfsDirectoryEntry &directoryEntry = directoryBlock->entries[j];
            if (directoryEntry.name[0] == '\0')
            {
                break;
            }

            std::string_view fileNameBase;
            uint32_t pathIndex = entryToPathIndex[directoryEntry.directoryIndex];
            if (pathIndex != 0xFFFFFFFF)
            {
                fileNameBase = directoryPaths[pathIndex];
            }

            std::string_view fileName(directoryEntry.name, directoryEntry.flags.nameLength & 0x3F);
            if (directoryEntry.flags.directory)
            {
                if (entryCount < 0x10000)
                {
                    std::string dirPath;
                    dirPath.reserve(fileNameBase.size() + fileName.size() + 1);
                    dirPath.append(fileNameBase);
                    dirPath.append(fileName);
                    dirPath.push_back('/');
                    directoryPaths.push_back(std::move(dirPath));
                    entryToPathIndex[entryCount] = (uint32_t)(directoryPaths.size() - 1);
                }
                entryCount++;
                continue;
            }

            uint32_t fileBlockIndex = 0; // dummy
            uint32_t fileBlockCount = 0; // dummy

            std::string fullPath;
            fullPath.reserve(fileNameBase.size() + fileName.size());
            fullPath.append(fileNameBase);
            fullPath.append(fileName);
            fileMap[std::move(fullPath)] = { directoryEntry.length, fileBlockIndex, fileBlockCount };
            entryCount++;
        }
        tableBlockIndex++; // simplified iteration
    }
}

TEST_CASE("STFS parsing performance benchmark") {
    // Generate dummy STFS data
    const uint32_t NUM_BLOCKS = 1000;
    std::vector<uint8_t> stfsData(NUM_BLOCKS * sizeof(StfsDirectoryBlock));

    // Fill with entries
    StfsDirectoryBlock* blocks = (StfsDirectoryBlock*)stfsData.data();
    for (uint32_t i = 0; i < NUM_BLOCKS; i++) {
        for (uint32_t j = 0; j < StfsEntriesPerDirectoryBlock; j++) {
            StfsDirectoryEntry& entry = blocks[i].entries[j];
            memset(&entry, 0, sizeof(entry));

            // Create some directories
            if (j % 10 == 0) {
                entry.flags.directory = 1;
                strcpy(entry.name, "dir");
                entry.flags.nameLength = 3;
            } else {
                entry.flags.directory = 0;
                strcpy(entry.name, "file.txt");
                entry.flags.nameLength = 8;
            }
            // Add variety to index
            entry.directoryIndex = (i * StfsEntriesPerDirectoryBlock + j) % 100;
        }
    }

    const int ITERATIONS = 1000;

    auto start_orig = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < ITERATIONS; i++) {
        parse_original(stfsData.data(), 0, NUM_BLOCKS, 0, stfsData.size());
    }
    auto end_orig = std::chrono::high_resolution_clock::now();
    auto duration_orig = std::chrono::duration_cast<std::chrono::milliseconds>(end_orig - start_orig).count();

    auto start_opt = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < ITERATIONS; i++) {
        parse_optimized(stfsData.data(), 0, NUM_BLOCKS, 0, stfsData.size());
    }
    auto end_opt = std::chrono::high_resolution_clock::now();
    auto duration_opt = std::chrono::duration_cast<std::chrono::milliseconds>(end_opt - start_opt).count();

    std::cout << "Original duration: " << duration_orig << "ms" << std::endl;
    std::cout << "Optimized duration: " << duration_opt << "ms" << std::endl;

    double improvement = ((double)duration_orig - duration_opt) / duration_orig * 100.0;
    std::cout << "Improvement: " << improvement << "%" << std::endl;

    CHECK(duration_opt <= duration_orig);
}
