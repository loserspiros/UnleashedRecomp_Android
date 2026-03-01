<p align="center">
    <img src="https://raw.githubusercontent.com/hedge-dev/UnleashedRecompResources/refs/heads/main/images/logo/Logo.png" width="512"/>
</p>

<h1 align="center">Sonic Unleashed Recompiled: Multi-Platform</h1>

<p align="center">
  <strong>The definitive native port of the Xbox 360 classic, optimized for Android, Linux, and Windows.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Platform-Android_|_Linux_|_Windows-blue?style=for-the-badge&logo=android" alt="Platforms"/>
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

This fork pushes the boundaries of the recompilation engine with advanced optimizations and platform-native features:

### 🚀 Performance & Parallelism
- **Intel TBB Acceleration:** Leveraging **Intel Threading Building Blocks** and C++17 parallel execution policies to accelerate asset loading, hashing, and GPU pipeline pre-compilation.
- **Asynchronous Pipeline Compilation:** Eliminates gameplay stutters by pre-compiling graphics pipelines (MSAA, Gaussian Blur, Motion Blur) in the background.
- **O(1) Engine Lookups:** Replaced iterative search patterns with high-performance hash-based lookups for achievements and mod assets.
- **Zero-Allocation I/O:** Highly optimized **STFS** and **SVOD** (XContent) parsing that eliminates redundant string allocations and utilizes memory-mapped I/O.
- **Mod Lookup Cache:** Thread-local cache in the `ModLoader` to drastically reduce file system overhead in modded environments.

### 🎮 Platform-Native Features
- **Android Excellence:**
    - **Sustained Performance Mode:** Integrated frequency locking to prevent thermal throttling.
    - **Low-Latency Audio:** Dedicated **AAudio** and **Oboe** backends.
    - **Native Touch Controls:** Fully customized multi-touch overlay.
- **Desktop Mastery:**
    - Full support for **Linux (including Steam Deck)** and **Windows**.
    - Optimized for **High-Refresh-Rate** displays and native Vulkan 1.2 rendering.
- **Modern UX:**
    - Built-in **Achievement Overlay** faithfully recreated.
    - **Resolution Scaling** and native **Ultrawide/Aspect Ratio** patches.
    - **Universal Save Redirection** for seamless persistence.

---

## 📋 System Requirements

| Requirement | Android | Windows / Linux |
| :--- | :--- | :--- |
| **Architecture** | ARM64 (arm64-v8a) REQUIRED | x86-64 (Amd64) |
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
3.  Select your target OS and provide URLs for your assets (**ZIP, ISO, or XEX**).
4.  The CI handles all extraction, patching, and preparation, providing a ready-to-use artifact.

### 💻 Manual Build (Developer Path)

#### 📦 Prerequisites (Dependencies)
To build the project locally, ensure you have the following installed:
- **Build Tools:** `cmake` (3.22+), `git`, `ninja-build`, `ccache`.
- **Compilers:**
    - **Linux/Android:** `Clang 18+` or `gcc-13+`.
    - **Windows:** `Visual Studio 2022` with **Clang-cl** and **LLVM 18+**.
- **Libraries:** `libtbb-dev`, `libcurl4-openssl-dev`, `libfreetype-dev`.
- **Android Specific:** Android SDK, **NDK 25.2.9519653**, and **Java 17**.

#### 🛠️ Build Steps

##### **Windows** (PowerShell)
```powershell
# Build using the Clang preset
cmake --preset x64-Clang-Release
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
*Sonic Unleashed Recompiled* is an unofficial fan-made project. It is not affiliated with, authorized, or endorsed by SEGA® or Sonic Team™. This software is for educational and interoperability purposes and requires legally owned game assets to function.
