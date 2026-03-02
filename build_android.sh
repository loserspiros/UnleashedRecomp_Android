#!/bin/bash
set -e

# Build script for Android APK

# Make sure we are in the project root
cd "$(dirname "$0")"

mkdir -p ./UnleashedRecompLib/private

# Bootstrap vcpkg
echo "Bootstrapping vcpkg..."
./thirdparty/vcpkg/bootstrap-vcpkg.sh

# Apply all patches
if [ -f "./apply_patches.sh" ]; then
    chmod +x apply_patches.sh
    ./apply_patches.sh
else
    echo "Error: apply_patches.sh not found!"
    false
fi

# Build host tools if they don't exist
if [ ! -f "./build_tools/bin/XenosRecomp" ]; then
    echo "Building host tools..."
    chmod +x build_tools.sh
    ./build_tools.sh
fi

# Handle private assets
if [ -d "private" ]; then
    echo "Processing local 'private' directory..."
    # Copy all contents to the build directory
    cp -rv private/* ./UnleashedRecompLib/private/ 2>/dev/null || true

    # Recursive extraction (Max 5 levels)
    echo "Checking for nested archives/ISOs/STFS in ./UnleashedRecompLib/private/..."
    for i in {1..5}; do
        nested=$(find ./UnleashedRecompLib/private -type f \( -iname "*.iso" -o -iname "*.7z" -o -iname "*.zip" -o -iname "*.rar" -o -iname "TU_*" -o -iname "*.tar*" -o -iregex ".*/[0-9A-F]\{8,42\}" \) -not -name "*.skipped" -not -name "*.extracted" | head -n 1)

        if [ -z "$nested" ]; then
            break
        fi

        echo "Processing nested item (iteration $i): $nested"

        filename=$(basename "$nested")
        extension="${filename##*.}"
        is_iso=0
        if [[ "$extension" =~ ^(iso|ISO)$ ]]; then
            is_iso=1
        fi

        if 7z x -y "$nested" -o./UnleashedRecompLib/private/ > /dev/null 2>&1; then
            echo "Successfully extracted with 7z: $nested"
            mv "$nested" "${nested}.extracted"
        elif [ "$is_iso" -eq 1 ] && python3 tools/extract_xgd.py "$nested" ./UnleashedRecompLib/private/; then
            echo "Successfully extracted with extract_xgd.py: $nested"
            mv "$nested" "${nested}.extracted"
        elif [ "$is_iso" -eq 0 ] && python3 tools/extract_stfs.py "$nested" ./UnleashedRecompLib/private/; then
            echo "Successfully extracted with extract_stfs.py: $nested"
            mv "$nested" "${nested}.extracted"
        else
            echo "Warning: Failed to extract $nested, skipping..."
            mv "$nested" "${nested}.skipped"
        fi
    done

    # Finalization and normalization
    finalize_file() {
        local filename="$1"
        local target_path="./UnleashedRecompLib/private/$filename"
        local found_file=$(find ./UnleashedRecompLib/private -type f -iname "$filename" | { grep -vFx "$target_path" || true; } | head -n 1)
        local candidate_count=$(find ./UnleashedRecompLib/private -type f -iname "$filename" | { grep -vFx "$target_path" || true; } | wc -l)
        if [ "$candidate_count" -gt 1 ]; then
            echo "Warning: Multiple candidates for $filename found. Using the first one."
            find ./UnleashedRecompLib/private -type f -iname "$filename" | { grep -vFx "$target_path" || true; }
        fi

        if [ -n "$found_file" ]; then
            echo "Found $filename at $found_file, moving to root..."
            mv -f "$found_file" "$target_path"
        fi

        local root_file=$(find ./UnleashedRecompLib/private -maxdepth 1 -type f -iname "$filename" | head -n 1)
        if [ -n "$root_file" ] && [ "$root_file" != "$target_path" ]; then
             mv -f "$root_file" "$target_path"
        fi
    }

    finalize_file "default.xex"
    finalize_file "default.xexp"
    finalize_file "shader.ar"
else
    echo "Warning: 'private' directory not found. Using existing files in UnleashedRecompLib/private if present."
fi

# Verification
if [ ! -f "./UnleashedRecompLib/private/default.xex" ] || [ ! -f "./UnleashedRecompLib/private/shader.ar" ]; then
    echo "Error: Mandatory assets (default.xex, shader.ar) are missing!"
    echo "Please place them in a 'private' directory at the root and run again."
    false
fi

# Build APK
echo "Building APK..."
if [ -z "$ANDROID_NDK_HOME" ] && [ -d "$ANDROID_HOME/ndk" ]; then
    NDK_VERSION=$(ls "$ANDROID_HOME/ndk" | tail -n 1)
    if [ -n "$NDK_VERSION" ]; then
        export ANDROID_NDK_HOME="$ANDROID_HOME/ndk/$NDK_VERSION"
        echo "Auto-detected ANDROID_NDK_HOME: $ANDROID_NDK_HOME"
    fi
fi

cd android
./gradlew assembleDebug

echo "Build complete!"
echo "APK located at: android/app/build/outputs/apk/debug/app-debug.apk"
