import sys

with open('.github/workflows/release.yml', 'r') as f:
    content = f.read()

search_text = """          # Recursive extraction: check for archives, ISOs, or STFS containers
          echo "Checking for archives/ISOs/STFS in ./UnleashedRecompLib/private/..."
          ls -R ./UnleashedRecompLib/private/
          # Max 5 levels of nesting
          for i in {1..25}; do
            # Find files that look like archives, STFS, or our downloads
            nested=$(find ./UnleashedRecompLib/private -type f \( -iname "*.iso" -o -iname "*.7z" -o -iname "*.zip" -o -iname "*.rar" -o -iname "TU_*" -o -iname "*.tar*" -o -iname "download_*" -o -iregex ".*/[0-9A-F]\{8,42\}" \) -not -name "*.skipped" -not -name "*.extracted" | head -n 1)

            if [ -z "$nested" ]; then
              break
            fi

            echo "Processing item (iteration $i): $nested"

            success=0
            # Try specialized extractors first to avoid 7z incorrectly "succeeding" on ISOs/STFS (extracting only Video partition)
            if python3 tools/extract_xgd.py "$nested" ./UnleashedRecompLib/private/ ; then
              echo "Successfully extracted with extract_xgd.py: $nested"
              success=1
            elif python3 tools/extract_stfs.py "$nested" ./UnleashedRecompLib/private/ ; then
              echo "Successfully extracted with extract_stfs.py: $nested"
              success=1
            elif 7z x -y "$nested" -o./UnleashedRecompLib/private/ ; then
              echo "Successfully extracted with 7z: $nested"
              success=1
            fi

            if [ "$success" -eq 1 ]; then
              mv "$nested" "${nested}.extracted"
            else
              echo "Warning: Failed to extract $nested with any tool, skipping..."
              mv "$nested" "${nested}.skipped"
            fi
          done

          # Final search and move to ensure files are at the root of private/ and lowercase
          echo "Organizing and normalizing files in ./UnleashedRecompLib/private/..."

          echo "Current contents of ./UnleashedRecompLib/private/ before finalization:"
          finalize_file() {
            local filename="$1"
            local target_path="./UnleashedRecompLib/private/$filename"

              # Find all candidates case-insensitively
            local candidates=$(find ./UnleashedRecompLib/private -type f -iname "$filename" | { grep -vFx "$target_path" || true; })
            local candidate_count=$(echo "$candidates" | grep -v "^$" | wc -l || true)

            if [ "$candidate_count" -gt 0 ]; then
            local found_file=""
            if [ "$candidate_count" -gt 1 ]; then
            echo "Warning: Multiple candidates for $filename found:"
            echo "$candidates"
              # Prioritization: Prefer files NOT in 'game' or 'base' folders (likely TUs)
              found_file=$(echo "$candidates" | grep -vE "/(game|base)/" | head -n 1)
            if [ -z "$found_file" ]; then
              found_file=$(echo "$candidates" | head -n 1)
            fi
            echo "Selected: $found_file"
            else
              found_file="$candidates"
            fi

            if [ -n "$found_file" ]; then
            echo "Moving $found_file to root as $filename..."
            mv -f "$found_file" "$target_path"
            fi
            fi

              # If it's already at the root but with wrong case, fix it
            local root_file=$(find ./UnleashedRecompLib/private -maxdepth 1 -type f -iname "$filename" | head -n 1)
            if [ -n "$root_file" ] && [ "$root_file" != "$target_path" ]; then
            echo "Fixing case for $root_file -> $target_path"
            mv -f "$root_file" "$target_path"
            fi
          }

          finalize_file "default.xex"
          finalize_file "default.xexp"
          ls -R ./UnleashedRecompLib/private/
          finalize_file "shader.ar\"\"\"

replacement_text = \"\"\"          # Recursive extraction: check for archives, ISOs, or STFS containers
          echo "Checking for archives/ISOs/STFS in ./UnleashedRecompLib/private/..."
          ls -R ./UnleashedRecompLib/private/
          # Max 25 iterations for deep nesting
          for i in {1..25}; do
            # Find files that look like archives, STFS, or our downloads
            # Prioritize ISOs and hex-named STFS files in the search
            nested=$(find ./UnleashedRecompLib/private -type f \\( -iname "*.iso" -o -iregex ".*/[0-9A-F]\\\\{8,42\\\\}" \\) -not -name "*.skipped" -not -name "*.extracted" | head -n 1)
            if [ -z "$nested" ]; then
              nested=$(find ./UnleashedRecompLib/private -type f \\( -iname "*.7z" -o -iname "*.zip" -o -iname "*.rar" -o -iname "TU_*" -o -iname "*.tar*" -o -iname "download_*" \\) -not -name "*.skipped" -not -name "*.extracted" | head -n 1)
            fi

            if [ -z "$nested" ]; then
              break
            fi

            echo "Processing item (iteration $i): $nested"

            # Count files before extraction to verify if something was actually added
            before_count=$(find ./UnleashedRecompLib/private -type f | wc -l)

            success=0
            # Strictly use specialized extractors for ISOs and STFS
            if [[ "$nested" =~ \\.[Ii][Ss][Oo]$ ]]; then
              echo "Attempting specialized ISO extraction for: $nested"
              if python3 tools/extract_xgd.py "$nested" ./UnleashedRecompLib/private/ ; then
                echo "Successfully extracted with extract_xgd.py: $nested"
                success=1
              fi
            elif [[ "$nested" =~ /[0-9A-Fa-f]{8,42}$ ]] || [[ "$nested" =~ [Tt][Uu]_ ]]; then
              echo "Attempting specialized STFS extraction for: $nested"
              if python3 tools/extract_stfs.py "$nested" ./UnleashedRecompLib/private/ ; then
                echo "Successfully extracted with extract_stfs.py: $nested"
                success=1
              fi
            fi

            # Fallback to 7z ONLY for standard archives, NOT for ISOs
            if [ "$success" -eq 0 ] && [[ ! "$nested" =~ \\.[Ii][Ss][Oo]$ ]]; then
              echo "Attempting 7z extraction for: $nested"
              if 7z x -y "$nested" -o./UnleashedRecompLib/private/ ; then
                echo "Successfully extracted with 7z: $nested"
                success=1
              fi
            fi

            # Verification: did we actually extract anything?
            after_count=$(find ./UnleashedRecompLib/private -type f | wc -l)
            if [ "$success" -eq 1 ] && [ "$after_count" -le "$before_count" ]; then
              echo "Warning: Extraction reported success but no new files were found. This might be an empty archive or failed extraction."
              # We don't mark as failed yet, as some archives might be empty, but it's suspicious
            fi

            if [ "$success" -eq 1 ]; then
              mv "$nested" "${nested}.extracted"
            else
              echo "Warning: Failed to extract $nested with any suitable tool, skipping..."
              mv "$nested" "${nested}.skipped"
            fi
          done

          # Final search and move to ensure files are at the root of private/ and lowercase
          echo "Organizing and normalizing files in ./UnleashedRecompLib/private/..."

          finalize_file() {
            local filename="$1"
            local target_path="./UnleashedRecompLib/private/$filename"

            echo "Searching for $filename (case-insensitive) in private/..."
            # Find all candidates case-insensitively, excluding the target path itself
            local candidates=$(find ./UnleashedRecompLib/private -type f -iname "$filename" | { grep -vFx "$target_path" || true; })
            local candidate_count=$(echo "$candidates" | grep -v "^$" | wc -l || true)

            if [ "$candidate_count" -gt 0 ]; then
              local found_file=""
              if [ "$candidate_count" -gt 1 ]; then
                echo "Warning: Multiple candidates for $filename found:"
                echo "$candidates"
                # Prioritization: Prefer files NOT in 'game' or 'base' folders (likely TUs or higher priority)
                found_file=$(echo "$candidates" | grep -vE "/(game|base)/" | head -n 1)
                if [ -z "$found_file" ]; then
                  found_file=$(echo "$candidates" | head -n 1)
                fi
                echo "Selected priority candidate: $found_file"
              else
                found_file="$candidates"
              fi

              if [ -n "$found_file" ]; then
                echo "Moving $found_file to $target_path"
                mv -f "$found_file" "$target_path"
              fi
            fi

            # Final check/fix for case at root
            local root_file=$(find ./UnleashedRecompLib/private -maxdepth 1 -type f -iname "$filename" | head -n 1)
            if [ -n "$root_file" ] && [ "$root_file" != "$target_path" ]; then
              echo "Fixing case for $root_file -> $target_path"
              mv -f "$root_file" "$target_path"
            fi
          }

          finalize_file "default.xex"
          finalize_file "default.xexp"
          finalize_file "shader.ar\"\"\"

if search_text in content:
    new_content = content.replace(search_text, replacement_text)
    with open('.github/workflows/release.yml', 'w') as f:
        f.write(new_content)
    print("Workflow updated successfully")
else:
    print("Search text not found")
    sys.exit(1)
