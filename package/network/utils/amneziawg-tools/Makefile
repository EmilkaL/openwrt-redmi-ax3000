include $(TOPDIR)/rules.mk

PKG_NAME:=amneziawg-tools
PKG_VERSION:=3.1.20260812
PKG_RELEASE:=1
PKG_SOURCE_VERSION:=ee0f0a9aa34ff0a0da4b3433b9512781cfe02843
PKG_SOURCE:=$(PKG_NAME)-$(PKG_SOURCE_VERSION).tar.gz
PKG_SOURCE_URL:=https://codeload.github.com/amnezia-vpn/amneziawg-tools/tar.gz
PKG_SOURCE_URL_FILE:=$(PKG_SOURCE_VERSION)
PKG_HASH:=22438f231d39ea27e4bdc69707ec3103357f3cecc9ad3eecba18a61e5b39c9b9
PKG_BUILD_DIR:=$(BUILD_DIR)/$(PKG_NAME)-$(PKG_SOURCE_VERSION)
PKG_LICENSE:=GPL-2.0-only Apache-2.0
PKG_LICENSE_FILES:=COPYING
PKG_BUILD_PARALLEL:=1

AWG_OPENWRT_VERSION:=03b62269e2edc168504f057cffaafda11b25ed92
AWG_OPENWRT_SOURCE:=awg-openwrt-$(AWG_OPENWRT_VERSION).tar.gz

include $(INCLUDE_DIR)/package.mk

define Download/awg-openwrt-integration
  FILE:=$(AWG_OPENWRT_SOURCE)
  URL:=https://codeload.github.com/Slava-Shchipunov/awg-openwrt/tar.gz
  URL_FILE:=$(AWG_OPENWRT_VERSION)
  HASH:=5705ecb06b38b7494f4c0731ffe09e5686867451f9f67435bad6184900386135
endef

define Package/amneziawg-tools
  SECTION:=net
  CATEGORY:=Network
  SUBMENU:=VPN
  TITLE:=AmneziaWG tools and netifd integration
  URL:=https://github.com/amnezia-vpn/amneziawg-tools
  DEPENDS:=+kmod-amneziawg +ip-full +resolveip
endef

MAKE_PATH:=src
MAKE_VARS+=PLATFORM=linux

define Build/Prepare
	$(call Build/Prepare/Default)
	$(TAR) -C $(PKG_BUILD_DIR) -xzf $(DL_DIR)/$(AWG_OPENWRT_SOURCE)
endef

define Package/amneziawg-tools/install
	$(INSTALL_DIR) $(1)/usr/bin $(1)/lib/netifd/proto
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/src/wg $(1)/usr/bin/awg
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/awg-openwrt-$(AWG_OPENWRT_VERSION)/amneziawg-tools/files/amneziawg_watchdog $(1)/usr/bin/
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/awg-openwrt-$(AWG_OPENWRT_VERSION)/amneziawg-tools/files/amneziawg.sh $(1)/lib/netifd/proto/
endef

$(eval $(call Download,awg-openwrt-integration))
$(eval $(call BuildPackage,amneziawg-tools))
