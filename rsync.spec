Name:           rsync
Version:        3.2.3
Release:        1
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
BuildRequires:  lz4-devel openssl-devel libzstd-devel
Provides:       bundled(zlib) = 1.2.8 rsync-daemon
Obsoletes:      rsync-daemon
%{?systemd_requires}

Patch1: backport-Work-around-glibc-lchmod-issue-a-better-way.patch

%description
Rsync is an open source utility that provides fast incremental file transfer.
It uses the "rsync algorithm" which provides a very fast method for bringing
remote files into sync. It does this by sending just the differences in the
files across the link, without requiring that both sets of files are present
at one of the ends of the link beforehand.

%package_help

%prep
%autosetup -b 1 -n %{name}-%{version} -p1

patch -p1 -i patches/copy-devices.diff

%build
%configure --disable-xxhash
%make_build

%check
make check
chmod -x support/*

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
%doc tech_report.tex
%doc support/*
%license COPYING
%config(noreplace) %{_sysconfdir}/*.conf
%config(noreplace) %{_sysconfdir}/sysconfig/rsyncd
%{_unitdir}/rsyncd*
%{_bindir}/rsync*
%{_bindir}/rsync

%files help
%{_mandir}/man1/%{name}.1*
%{_mandir}/man1/%{name}-ssl.1*
%{_mandir}/man5/rsyncd.conf.5*

%changelog
* Fri Jan 22 2021 yixiangzhike <zhangxingliang3@huawei.com> - 3.2.3-1
- Type:requirement
- ID:NA
- SUG:NA
- DESC:update to 3.2.3

* Tue Jul 28 2020 Liquor <lirui130@huawei.com> - 3.2.1-1
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:update to 3.2.1

* Fri Sep 27 2019 chengquan<chengquan3@huawei.com> - 3.1.3-6
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:fix spec rule in openeuler

* Mon Sep 09 2019 openEuler Buildteam <buildteam@openeuler.org> - 3.1.3-5
- Package init
