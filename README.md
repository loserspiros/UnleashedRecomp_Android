<p align="center">
    <img src="https://raw.githubusercontent.com/hedge-dev/UnleashedRecompResources/refs/heads/main/images/logo/Logo.png" width="512"/>
</p>

<h1 align="center">Sonic Unleashed Recompiled: Multi-Platform</h1>

<p align="center">
  <strong>The definitive native port of the Xbox 360 classic, optimized for Android, Linux, and Windows.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Platform-Android_|_Linux_|_Windows-blue?style=for-the-badge&logo=android" alt="Platforms"/>
  <img src="https://img.shields.io/badge/Architecture-ARM64_|_x86--64-blue?style=for-the-badge" alt="Arch"/>
  <img src="https://img.shields.io/badge/Vulkan-1.2+-red?style=for-the-badge&logo=vulkan" alt="Vulkan"/>
  <img src="https://img.shields.io/badge/Status-Experimental_WIP-orange?style=for-the-badge" alt="Status"/>
</p>

---

## 🌟 Overview

This project is a high-fidelity, static recompilation of the Xbox 360 version of **Sonic Unleashed**. By translating original PowerPC binaries into native machine code (ARM64/x86-64), this port achieves near-native performance on modern hardware. Experience the classic game with modern enhancements like high resolution, ultrawide support, and native controls across all your devices.

> [!IMPORTANT]
> **Game assets are NOT included.** You must provide your own legally acquired Xbox 360 copy of *Sonic Unleashed* and its updates.

---

## ✨ Key Architectural Enhancements

This fork pushes the boundaries of the recompilation engine with advanced optimizations:

### 🚀 Performance & Parallelism
- **Parallel Execution Engine:** Leveraging **Intel TBB** and C++17 parallel algorithms to accelerate asset loading, hashing, and GPU pipeline pre-compilation.
- **Background Pipeline Compilation:** Eliminates gameplay stutters by pre-compiling graphics pipelines (MSAA, Blur, etc.) in the background.
- **O(1) Engine Lookups:** Replaced iterative search patterns with hash-based lookups for achievements and mod assets.
- **Zero-Allocation I/O:** Optimized **STFS** and **SVOD** (XContent) parsing that eliminates redundant string allocations and utilizes memory-mapped I/O.
- **Thread-Local Caching:** Highly efficient `ModLoader` with thread-local lookup caches to prevent file system contention.

### 🎮 Platform-Native Features
- **Android Excellence:** Native integration with **Sustained Performance Mode**, low-latency **AAudio/Oboe** audio, and a customizable **Touch Overlay**.
- **Desktop Mastery:** Full support for **Linux (including Steam Deck)** and **Windows** with native Vulkan 1.2 rendering and high-refresh-rate display compatibility.
- **Modern UX:** Built-in **Achievement Overlay**, **Resolution Scaling**, **Ultrawide Aspect Ratio** patches, and **Universal Save Redirection**.
- **Modding Support:** Native compatibility with the **Hedge Mod Manager** ecosystem.

---

## 📋 System Requirements

| Requirement | Android | Windows / Linux |
| :--- | :--- | :--- |
| **Architecture** | ARM64 (v8-a) REQUIRED | x86-64 (Amd64) |
| **OS Version** | Android 8.0+ (API 26) | Win 10/11 / Ubuntu 24.04+ |
| **Graphics API** | Vulkan 1.2+ REQUIRED | Vulkan 1.2+ |
| **RAM** | 4 GB (Strict Guest Allocation) | 8 GB+ Recommended |
| **Storage** | 10-15 GB (High-speed internal) | 10-15 GB |

---

## 🚀 Getting Started

### 🌐 GitHub Actions (The Easiest Way)
Build for any platform without local setup:
1.  **Fork** this repository.
2.  Go to the **Actions** tab -> **Release** workflow -> **Run workflow**.
3.  Select your target OS and provide URLs for your game assets (ZIP/ISO/XEX).
4.  The CI handles all the heavy lifting and provides a ready-to-use artifact.

### 💻 Manual Build (Developer Path)

#### 📦 Prerequisites (Common)
- `cmake` (3.22+), `git`, `curl`, `freetype`, `zstd`.
- `libtbb-dev` (Intel Threading Building Blocks).

#### 📦 Platform Specifics
- **Windows:** Visual Studio 2022 with **Clang-cl**, **LLVM 18+**, and **Ninja**.
- **Linux:** `gcc-13` / `g++-13` (or Clang 18+), Vulkan SDK, and `ccache`.
- **Android:** Android SDK, **NDK 25.2.9519653**, and **Java 17**.

#### 🛠️ Build Steps

##### **Windows** (PowerShell)
```powershell
mkdir build; cd build
cmake .. --preset x64-Clang-Release
cmake --build . --config Release --parallel
```

##### **Linux** (Bash)
```bash
# Standard Build
mkdir build; cd build
cmake .. --preset linux-release
cmake --build . --config Release --parallel

# Flatpak Build
flatpak-builder --user --install --force-clean build flatpak/io.github.hedge_dev.unleashedrecomp.json
```

##### **Android** (Linux/WSL)
```bash
# 1. Build host-side tools first
chmod +x ./build_tools.sh && ./build_tools.sh

# 2. Set NDK path and build APK
export ANDROID_NDK_HOME=/path/to/ndk-25.2.9519653
chmod +x ./build_android.sh && ./build_android.sh
```

---

## ⚖️ Disclaimer
*Sonic Unleashed Recompiled* is an unofficial fan-made project. It is not affiliated with, authorized, or endorsed by SEGA® or Sonic Team™. All trademarks belong to their respective owners.
