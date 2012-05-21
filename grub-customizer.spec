Name:           grub-customizer
Version:        2.5.6
Release:        1%{?dist}
Summary:        Grub Customizer is a graphical interface to configure the grub2/burg settings

License:        GPLv3
URL:            https://launchpad.net/grub-customizer
Source0:        https://launchpad.net/grub-customizer/2.5/%{version}/+download/%{name}_%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  gtkmm24-devel >= 2.18
BuildRequires:  gettext
BuildRequires:  openssl-devel

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
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

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

%files -f %{name}.lang
%defattr (-,root,root,0755)
%doc README COPYING changelog
%config %{_sysconfdir}/%{name}/*
%{_bindir}/%{name}
%{_libdir}/grubcfg-proxy
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_mandir}/man1/%{name}.1*
%{_datadir}/polkit-1/actions/net.launchpad.danielrichter2007.pkexec.grub-customizer.policy


%changelog
* Sat May 12 2012 Vasiliy N. Glazov <vascom2@gmail.com> 2.5.6-1.R
- Drop patch
- Update to 2.5.6

* Fri May 11 2012 Vasiliy N. Glazov <vascom2@gmail.com> 2.5.5-1.R
- Initial release
