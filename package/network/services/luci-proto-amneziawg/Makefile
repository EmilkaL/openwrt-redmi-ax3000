include $(TOPDIR)/rules.mk

PKG_NAME:=luci-proto-amneziawg
PKG_VERSION:=3.1.0
PKG_RELEASE:=1
PKG_SOURCE_VERSION:=03b62269e2edc168504f057cffaafda11b25ed92
PKG_SOURCE:=awg-openwrt-$(PKG_SOURCE_VERSION).tar.gz
PKG_SOURCE_URL:=https://codeload.github.com/Slava-Shchipunov/awg-openwrt/tar.gz
PKG_SOURCE_URL_FILE:=$(PKG_SOURCE_VERSION)
PKG_HASH:=5705ecb06b38b7494f4c0731ffe09e5686867451f9f67435bad6184900386135
PKG_BUILD_DIR:=$(BUILD_DIR)/$(PKG_NAME)-$(PKG_SOURCE_VERSION)
PKG_LICENSE:=Apache-2.0
PKGARCH:=all

include $(INCLUDE_DIR)/package.mk

define Package/luci-proto-amneziawg
  SECTION:=luci
  CATEGORY:=LuCI
  SUBMENU:=6. Protocols
  TITLE:=LuCI support for AmneziaWG
  URL:=https://github.com/Slava-Shchipunov/awg-openwrt
  DEPENDS:=+amneziawg-tools +luci-base +luci-lib-uqr +rpcd-mod-ucode +ucode +resolveip
endef

define Build/Prepare
	$(INSTALL_DIR) $(PKG_BUILD_DIR)
	$(TAR) -C $(PKG_BUILD_DIR) --strip-components=1 -xzf $(DL_DIR)/$(PKG_SOURCE)
endef

define Build/Configure
endef

define Build/Compile
endef

define Package/luci-proto-amneziawg/install
	$(INSTALL_DIR) $(1)/www
	$(CP) $(PKG_BUILD_DIR)/luci-proto-amneziawg/htdocs/. $(1)/www/
	$(CP) $(PKG_BUILD_DIR)/luci-proto-amneziawg/root/. $(1)/
endef

$(eval $(call BuildPackage,luci-proto-amneziawg))
