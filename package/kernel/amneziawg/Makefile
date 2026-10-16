include $(TOPDIR)/rules.mk
include $(INCLUDE_DIR)/kernel.mk

PKG_NAME:=amneziawg
PKG_VERSION:=3.1.20260906
PKG_RELEASE:=1
PKG_SOURCE_VERSION:=4569c4c67f3a57414969260cafbbd04694fbaae0
PKG_SOURCE:=$(PKG_NAME)-$(PKG_SOURCE_VERSION).tar.gz
PKG_SOURCE_URL:=https://codeload.github.com/amnezia-vpn/amneziawg-linux-kernel-module/tar.gz
PKG_SOURCE_URL_FILE:=$(PKG_SOURCE_VERSION)
PKG_HASH:=6d7608935adbcdd4c6e9fed705951e2ee85311ac212a8e8f1274abcf9b06f83e
PKG_BUILD_DIR:=$(KERNEL_BUILD_DIR)/amneziawg-linux-kernel-module-$(PKG_SOURCE_VERSION)
PKG_LICENSE:=GPL-2.0-only
PKG_LICENSE_FILES:=COPYING
PKG_BUILD_PARALLEL:=1

include $(INCLUDE_DIR)/package.mk

define KernelPackage/amneziawg
  SUBMENU:=Network Support
  TITLE:=AmneziaWG VPN kernel module
  URL:=https://github.com/amnezia-vpn/amneziawg-linux-kernel-module
  DEPENDS:=+kmod-udptunnel4 +kmod-udptunnel6 +kmod-crypto-lib-chacha20poly1305 +kmod-crypto-lib-curve25519
  FILES:=$(PKG_BUILD_DIR)/src/amneziawg.ko
  AUTOLOAD:=$(call AutoProbe,amneziawg)
endef

define Build/Compile
	+$(KERNEL_MAKE) M="$(PKG_BUILD_DIR)/src" WIREGUARD_VERSION="$(PKG_VERSION)" modules
endef

$(eval $(call KernelPackage,amneziawg))
