include $(TOPDIR)/rules.mk

PKG_NAME:=ra80-vpn
PKG_VERSION:=1.0.0
PKG_RELEASE:=1
PKG_LICENSE:=MIT
PKGARCH:=all

include $(INCLUDE_DIR)/package.mk

define Package/ra80-vpn
  SECTION:=net
  CATEGORY:=Network
  SUBMENU:=VPN
  TITLE:=AmneziaWG selective routing for Xiaomi RA80V2
  DEPENDS:=+amneziawg-tools +dnsmasq-full +firewall4 +ip-full +nftables-json +kmod-nft-nat
endef

define Package/ra80-vpn/description
  Inactive until a private AmneziaWG peer is configured and explicitly enabled.
  Routes selected IPv4 destinations through AmneziaWG with an unreachable fallback,
  persistent DNS sets, forced local DNS, and an IPv6 forwarding guard.
endef

define Package/ra80-vpn/conffiles
/etc/config/ra80_vpn
endef

define Build/Compile
endef

define Package/ra80-vpn/install
	$(INSTALL_DIR) $(1)/usr/sbin $(1)/usr/share/ra80-vpn $(1)/etc/config $(1)/etc/init.d
	$(INSTALL_BIN) ./files/ra80-vpn $(1)/usr/sbin/ra80-vpn
	$(INSTALL_BIN) ./files/ra80-vpn.init $(1)/etc/init.d/ra80-vpn
	$(INSTALL_CONF) ./files/ra80_vpn.config $(1)/etc/config/ra80_vpn
	$(INSTALL_DATA) ./files/*.nft ./files/*.txt ./files/*.example $(1)/usr/share/ra80-vpn/
endef

$(eval $(call BuildPackage,ra80-vpn))
