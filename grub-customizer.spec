Name:           grub-customizer
Version:        4.0.2
Release:        1%{?dist}
Summary:        Grub Customizer is a graphical interface to configure the grub2/burg settings

License:        GPLv3
URL:            https://launchpad.net/grub-customizer
Source0:        https://launchpad.net/grub-customizer/4.0/%{version}/+download/%{name}_%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gtkmm30-devel
BuildRequires:  gettext
BuildRequires:  openssl-devel
BuildRequires:  libarchive-devel
BuildRequires:  desktop-file-utils

Requires:       grub2

%description
Grub Customizer is a graphical interface to configure the grub2/burg settings
with focus on the individual list order - without losing the dynamical behavior
of grub.

The goal of this project is to create a complete and intuitive graphical
grub2/burg configuration interface. The main feature is the boot entry list
configuration - but not simply by modified the grub.cfg: to keep the dynamical
configuration, this application will only edit the script order and generate
proxies (script output filter), if required.

%prep
%setup -q

%build
%cmake .
make %{?_smp_mflags}


%install
%make_install

desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}.desktop

cat > grub.cfg << EOF
MKCONFIG_CMD=grub2-mkconfig
INSTALL_CMD=grub2-install
MKFONT_CMD=grub2-mkfont
CFG_DIR=/etc/grub.d
OUTPUT_DIR=/boot/grub2
OUTPUT_FILE=/boot/grub2/grub.cfg
SETTINGS_FILE=/etc/default/grub

EOF
mkdir -p %{buildroot}%{_sysconfdir}/%{name}
install -m 0644 grub.cfg %{buildroot}%{_sysconfdir}/%{name}/grub.cfg

%find_lang %{name}

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache -f %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache -f %{_datadir}/icons/hicolor &>/dev/null || :

%files -f %{name}.lang
%doc README COPYING changelog
%config(noreplace) %{_sysconfdir}/%{name}
%{_bindir}/%{name}
%{_libdir}/grubcfg-proxy
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_mandir}/man1/%{name}.1*
%{_datadir}/polkit-1/actions/net.launchpad.danielrichter2007.pkexec.grub-customizer.policy


%changelog
* Thu Dec 26 2013 Vasiliy N. Glazov <vascom2@gmail.com> 4.0.2-1
- Update to 4.0.2

* Wed Mar 20 2013 Vasiliy N. Glazov <vascom2@gmail.com> 3.0.4-1
- Update to 3.0.4

* Thu Sep 13 2012 Vasiliy N. Glazov <vascom2@gmail.com> 3.0.2-1
- Update to 3.0.2

* Mon Jul 16 2012 Vasiliy N. Glazov <vascom2@gmail.com> 2.5.7-2
- add gtk-update-icon-cache scriptlet
- add desktop-file-validate and BR for it
- add patch for correct FSF address in sources
- clean spec

* Thu Jun 14 2012 Vasiliy N. Glazov <vascom2@gmail.com> 2.5.7-1
- Update to 2.5.7

* Sat May 12 2012 Vasiliy N. Glazov <vascom2@gmail.com> 2.5.6-1
- Drop patch
- Update to 2.5.6

* Fri May 11 2012 Vasiliy N. Glazov <vascom2@gmail.com> 2.5.5-1
- Initial release
