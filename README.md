<p align="center">
    <img src="https://raw.githubusercontent.com/hedge-dev/UnleashedRecompResources/refs/heads/main/images/logo/Logo.png" width="512"/>
</p>

<h1 align="center">Sonic Unleashed Recompiled: Multi-Platform</h1>

<p align="center">
  <strong>The definitive native port of the Xbox 360 classic, optimized for Android, Linux, and Windows.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Platform-Android_|_Linux_|_Windows-blue?style=for-the-badge&logo=android" alt="Platforms"/>
  <img src="https://img.shields.io/badge/Vulkan-1.2-red?style=for-the-badge&logo=vulkan" alt="Vulkan"/>
  <img src="https://img.shields.io/badge/Status-Experimental_WIP-orange?style=for-the-badge" alt="Status"/>
</p>

---

## 🌟 The Project

This repository contains a high-performance, static recompilation of the Xbox 360 version of **Sonic Unleashed**. By translating PowerPC binaries directly into native ARM64 or x86-64 machine code, this port achieves near-native execution speeds. Experience the classic "Hedgehog Engine" game with modern enhancements like resolution scaling, ultrawide support, and native low-latency audio across all your devices.

> [!IMPORTANT]
> **Game assets are NOT included.** You must provide your own legally acquired Xbox 360 copy of *Sonic Unleashed* and its updates.

---

## ✨ Cutting-Edge Enhancements

This fork pushes the boundaries of the recompilation engine with advanced optimizations and platform-native features:

### 🚀 Engine & Performance
- **Parallel execution engine:** Powered by **Intel TBB** and C++17 parallel algorithms to accelerate asset loading, hashing, and GPU pipeline pre-compilation.
- **Background Pipeline Compilation:** Background pre-compilation of graphics pipelines (MSAA, Blur, etc.) eliminates mid-game stutters.
- **O(1) Optimized Lookups:** Replaced iterative search patterns with hash-based lookups for achievements and mod assets, removing CPU bottlenecks.
- **Zero-Allocation I/O:** Highly optimized **STFS** and **SVOD** (XContent) parsing with zero-allocation string handling and memory-mapped reads.
- **Thread-Local Mod Caching:** Drastically reduces file system overhead in modded environments using the specialized `ModLoader` cache.

### 🎮 Platform-Specific Excellence
- **Android Integration:**
    - **Sustained Performance Mode:** Native API integration to lock CPU/GPU clocks and prevent thermal throttling.
    - **Optimized Android HID:** Refined native controller handling and low-latency input processing.
    - **Next-Gen Audio:** Full **AAudio** and **Oboe** backend integration for sub-millisecond audio response times.
    - **Native Touch Interface:** Fully customized multi-touch overlay for mobile-first play.
- **Desktop Mastery:**
    - Full support for **Linux (including Steam Deck)** and **Windows**.
    - Optimized for **High-Refresh-Rate** displays and native **Vulkan 1.2** rendering.
- **Modern UX Features:**
    - Built-in **Achievement Overlay** faithfully recreated.
    - Native support for **Resolution Scaling** and **Ultrawide Aspect Ratio** patches.
    - **Universal Save Redirection** for seamless persistence across OS updates.

---

## 📋 System Requirements

| Requirement | Android | Windows / Linux |
| :--- | :--- | :--- |
| **Architecture** | ARM64 (arm64-v8a) REQUIRED | x86-64 (Amd64) |
| **OS Version** | Android 8.0+ (API 26) | Win 10/11 / Ubuntu 24.04+ |
| **Graphics API** | Vulkan 1.2 REQUIRED | Vulkan 1.2+ |
| **RAM** | 4 GB (Strict Guest Allocation) | 8 GB+ Recommended |
| **Storage** | 10-15 GB (High-speed internal) | 10-15 GB |

---

## 🚀 Installation & Build Guide

### 🌐 GitHub Actions (Recommended)
Build for any platform without a local setup:
1.  **Fork** this repository.
2.  Navigate to the **Actions** tab -> **Release** workflow -> **Run workflow**.
3.  Select your target OS and provide URLs for your assets (**ZIP, ISO, or XEX**).
4.  The CI handles all extraction, patching, and preparation, providing a ready-to-use artifact.

### 💻 Manual Build (Developer Path)

#### 📦 Prerequisites
- **Common:** `cmake` (3.22+), `git`, `ninja-build`, `ccache`, `libtbb-dev`.
- **Android:** Android SDK, **NDK 25.2.9519653**, and **Java 17**.
- **Windows:** **Visual Studio 2022** with **Clang-cl** and **LLVM 18+**.
- **Linux:** `gcc-13` / `g++-13` and Vulkan development headers.

#### 🛠️ Build Steps

##### **Windows** (PowerShell)
```powershell
mkdir build; cd build
cmake .. --preset x64-Clang-Release
cmake --build out/build/x64-Clang-Release --config Release --parallel
```

##### **Linux** (Bash)
```bash
# Standard Build
cmake --preset linux-release
cmake --build out/build/linux-release --config Release --parallel

# Flatpak Build
flatpak-builder --user --install --force-clean build flatpak/io.github.hedge_dev.unleashedrecomp.json
```

##### **Android** (Linux/WSL Bash)
```bash
# 1. Build host-side tools first
chmod +x ./build_tools.sh && ./build_tools.sh

# 2. Set NDK path (REQUIRED)
export ANDROID_NDK_HOME=/path/to/android-sdk/ndk/25.2.9519653

# 3. Compile the APK
chmod +x ./build_android.sh && ./build_android.sh
```

---

## ⚖️ Disclaimer
*Sonic Unleashed Recompiled* is an unofficial fan-made project. It is not affiliated with, authorized, or endorsed by SEGA® or Sonic Team™. This project is intended for educational and interoperability purposes and requires legally owned game assets.
