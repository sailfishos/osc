# osc plugin support
%global osc_plugin_dir %{_prefix}/lib/osc-plugins
# for obs source services
%global obsroot %{_prefix}/lib/obs
%global obs_srcsvc_dir %{obsroot}/service
%global __python %{__python3}

Name:           osc
Summary:        Open Build Service Commander
Version:        0.167.1
Release:        0
License:        GPLv2+
URL:            https://github.com/openSUSE/osc
BuildArch:      noarch
Source0:        %{name}-%{version}.tar.bz2
	
# Backports from upstream	
## Fix various "osc chroot" regressions
Patch0001:      0001-fix-regression-in-osc-chroot.patch
# Proposed fixes
## Fix osc build --local-package runs
## From: https://github.com/openSUSE/osc/pull/573
Patch0101:      0101-Do-not-attempt-to-run-source-services-when-local-pac.patch
## Use html.escape instead of cgi.escape
## From: https://github.com/openSUSE/osc/pull/681
Patch0102:      0102-Swap-all-usage-of-cgi.escape-with-html.escape.patch
## Fix broken importsrcpkg for Python 3
## From: https://github.com/openSUSE/osc/pull/713
Patch0103:      0103-fix-broken-importsrcpkg-for-python3.patch

BuildRequires:  python3-devel	
BuildRequires:  python3-distro
BuildRequires:  rpm-python
Requires:       python3-distro
Requires:       rpm-python
Requires:       python3-m2crypto
Requires:       python3-lxml

%description
Commandline client for the Open Build Service. 
See http://en.opensuse.org/openSUSE:OSC, as well as
http://en.opensuse.org/openSUSE:Build_Service_Tutorial for a general
introduction.

%prep	
%autosetup -p1 -n %{name}-%{version}/osc

%build
%{py3_build}

%install
rm -rf %{buildroot}
%{py3_install}

%__ln_s osc-wrapper.py %{buildroot}%{_bindir}/osc
%__mkdir_p %{buildroot}%{_localstatedir}/lib/osc-plugins
%__mkdir_p %{buildroot}%{_datadir}/bash-completion/completions/
install -Dm0644 dist/complete.csh %{buildroot}%{_sysconfdir}/profile.d/osc.csh
install -Dm0644 dist/complete.sh %{buildroot}%{_datadir}/bash-completion/completions/osc
install -Dm0755 dist/osc.complete %{buildroot}%{_datadir}/osc/complete

mkdir -p %{buildroot}%{obs_srcsvc_dir}
mkdir -p %{buildroot}%{osc_plugin_dir}	
mkdir -p %{buildroot}%{_rpmconfigdir}/macros.d/

# osc rpm macros
cat > %{buildroot}%{_rpmconfigdir}/macros.d/macros.osc <<EOM
%%obs_srcsvc_dir %{obs_srcsvc_dir}
%%osc_plugin_dir %{osc_plugin_dir}
EOM

%files
%doc AUTHORS README TODO NEWS
%license COPYING
%{_bindir}/osc*
%{python_sitelib}/osc*
%{_sysconfdir}/profile.d/osc.csh
%{_datadir}/bash-completion/completions/osc
%dir %{_localstatedir}/lib/osc-plugins
%{_mandir}/man1/osc.*
%{_datadir}/osc
%{_rpmconfigdir}/macros.d/macros.osc
%dir %{obsroot}
%dir %{obs_srcsvc_dir}
%dir %{osc_plugin_dir}

