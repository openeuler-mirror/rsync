Name:           rsync
Version:        3.1.3
Release:        7
Summary:        Fast incremental file transfer utility
License:        GPLv3+
URL:            http://rsync.samba.org/
Source0:        https://download.samba.org/pub/rsync/src/rsync-%{version}%{?prerelease}.tar.gz
Source1:        https://download.samba.org/pub/rsync/src/rsync-patches-%{version}.tar.gz
Source2:        rsyncd.socket
Source3:        rsyncd.service
Source4:        rsyncd.conf
Source5:        rsyncd.sysconfig
Source6:        rsyncd@.service

BuildRequires:  git gcc systemd libacl-devel libattr-devel autoconf popt-devel
Provides:       bundled(zlib) = 1.2.8 rsync-daemon
Obsoletes:      rsync-daemon
%{?systemd_requires}

Patch0:         rsync-man.patch
Patch1:         rsync-noatime.patch
Patch6000:      Avoid-a-compiler-error-warning-about-shifting-a-nega.patch
Patch6001:      Need-to-mark-xattr-rules-in-get_rule_prefix.patch
Patch6002:      Fix-itemizing-of-wrong-dir-name-on-some-iconv-transf.patch
Patch6003:      Avoid-a-potential-out-of-bounds-read-in-daemon-mode-.patch
Patch6004:      Avoid-leaving-a-file-open-on-error-return.patch
Patch6005:      Fix-remove-source-files-sanity-check-w-copy-links-th.patch
Patch6006:      Fix-zlib-CVE-2016-9840.patch
Patch6007:      Fix-zlib-CVE-2016-9841.patch
Patch6008:      Fix-zlib-CVE-2016-9842.patch
Patch6009:      Fix-zlib-CVE-2016-9843.patch
Patch6010:      Fix-bug-in-try_dests_reg-that-Florian-Zumbiehl-point.patch
Patch6011:      Try-to-fix-the-iconv-crash-in-bug-11338.patch
Patch6012:      CVE-2017-17433.patch
Patch6013:      backport-Use-a-lock-to-not-fail-on-a-left-over-pid-file.patch 

%description
Rsync is an open source utility that provides fast incremental file transfer.
It uses the "rsync algorithm" which provides a very fast method for bringing
remote files into sync. It does this by sending just the differences in the
files across the link, without requiring that both sets of files are present
at one of the ends of the link beforehand.

%package_help

%prep
%autosetup -b 1 -n %{name}-%{version} -p1

patch -p1 -i patches/acls.diff
patch -p1 -i patches/xattrs.diff
patch -p1 -i patches/copy-devices.diff

chmod -x support/*

%build
%configure
%make_build

%install
%make_install

install -D -m644 %{SOURCE2} %{buildroot}/%{_unitdir}/rsyncd.socket
install -D -m644 %{SOURCE3} %{buildroot}/%{_unitdir}/rsyncd.service
install -D -m644 %{SOURCE4} %{buildroot}/%{_sysconfdir}/rsyncd.conf
install -D -m644 %{SOURCE5} %{buildroot}/%{_sysconfdir}/sysconfig/rsyncd
install -D -m644 %{SOURCE6} %{buildroot}/%{_unitdir}/rsyncd@.service

%pre

%preun
%systemd_preun rsyncd.service

%post
%systemd_post rsyncd.service

%postun
%systemd_postun_with_restart rsyncd.service

%files
%defattr(-,root,root)
%doc NEWS OLDNEWS README tech_report.tex
%doc support/*
%license COPYING
%config(noreplace) %{_sysconfdir}/*.conf
%config(noreplace) %{_sysconfdir}/sysconfig/rsyncd
%{_unitdir}/rsyncd*
%{_bindir}/rsync

%files help
%{_mandir}/man1/%{name}.1*
%{_mandir}/man5/rsyncd.conf.5*

%changelog
* Mon Dec 20 2021 yangzhuangzhuang<yangzhuangzhuang1@huawei.com> - 3.1.3-7
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:Fix the issue that the pid file cannot be rewritten

* Fri Sep 27 2019 chengquan<chengquan3@huawei.com> - 3.1.3-6
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:fix spec rule in openeuler

* Mon Sep 09 2019 openEuler Buildteam <buildteam@openeuler.org> - 3.1.3-5
- Package init
