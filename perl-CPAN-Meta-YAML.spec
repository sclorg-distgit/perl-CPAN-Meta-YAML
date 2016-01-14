%{?scl:%scl_package perl-CPAN-Meta-YAML}
%{!?scl:%global pkg_name %{name}}

Name:		%{?scl_prefix}perl-CPAN-Meta-YAML
Version:	0.010
Release:	3.sc1%{?dist}
Summary:	Read and write a subset of YAML for CPAN Meta files
License:	GPL+ or Artistic
Group:		Development/Libraries
URL:		http://search.cpan.org/dist/CPAN-Meta-YAML/
Source0:	http://search.cpan.org/CPAN/authors/id/D/DA/DAGOLDEN/CPAN-Meta-YAML-%{version}.tar.gz
Patch0:		CPAN-Meta-YAML-0.009-TM094.patch
Patch1:		CPAN-Meta-YAML-0.009-old-Test::More.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildArch:	noarch
BuildRequires:	%{?scl_prefix}perl(Carp)
BuildRequires:	%{?scl_prefix}perl(Exporter)
BuildRequires:	%{?scl_prefix}perl(ExtUtils::MakeMaker)
BuildRequires:	%{?scl_prefix}perl(File::Spec)
# Tests:
BuildRequires:	%{?scl_prefix}perl(IO::Handle)
BuildRequires:	%{?scl_prefix}perl(IPC::Open3)
BuildRequires:	%{?scl_prefix}perl(File::Spec::Functions)
BuildRequires:	%{?scl_prefix}perl(File::Temp)
BuildRequires:	%{?scl_prefix}perl(Test::More)
BuildRequires:	%{?scl_prefix}perl(YAML)
# Don't run extra tests when bootstrapping as many of those
# tests' dependencies build-require this package
%if 0%{?fedora} && 0%{!?perl_bootstrap:1} && ! ( 0%{?scl:1} )
BuildRequires:	%{?scl_prefix}perl(Test::CPAN::Meta)
BuildRequires:	%{?scl_prefix}perl(Test::Pod)
BuildRequires:	%{?scl_prefix}perl(Test::Requires)
BuildRequires:	%{?scl_prefix}perl(Test::Version)
%endif
%{?scl:%global perl_version %(scl enable %{scl} 'eval "`perl -V:version`"; echo $version')}
%{!?scl:%global perl_version %(eval "`perl -V:version`"; echo $version)}
Requires:	%{?scl_prefix}perl(:MODULE_COMPAT_%{perl_version})
Requires:	%{?scl_prefix}perl(Carp)
Requires:	%{?scl_prefix}perl(Exporter)

# We need to patch the test suite if we have Test::More < 0.94
%{?scl:%global quite_old_test_more %(scl enable %{scl} "perl -MTest::More -e 'print ((\\$Test::More::VERSION < 0.94) ? 1 : 0)'" 2>/dev/null || echo 0)}
%{!?scl:%global quite_old_test_more %(perl -MTest::More -e 'print ($Test::More::VERSION < 0.94 ? 1 : 0);' 2>/dev/null || echo 0)}
# We need to patch the test suite again if we have Test::More < 0.88
%{?scl:%global old_test_more %(scl enable %{scl} "perl -MTest::More -e 'print ((\\$Test::More::VERSION < 0.88) ? 1 : 0)'" 2>/dev/null || echo 0)}
%{!?scl:%global old_test_more %(perl -MTest::More -e 'print ($Test::More::VERSION < 0.88 ? 1 : 0);' 2>/dev/null || echo 0)}

%description
This module implements a subset of the YAML specification for use in reading
and writing CPAN metadata files like META.yml and MYMETA.yml. It should not be
used for any other general YAML parsing or generation task.

%prep
%setup -q -n CPAN-Meta-YAML-%{version}

# We need to patch the test suite if we have Test::More < 0.94
%if 00%{quite_old_test_more}
%patch0
%endif

# We need to patch the test suite again if we have Test::More < 0.88
%if 00%{old_test_more}
%patch1
%endif

%build
%{?scl:scl enable %{scl} "}
perl Makefile.PL INSTALLDIRS=vendor UNINST=0
%{?scl:"}
%{?scl:scl enable %{scl} "}
make %{?_smp_mflags}
%{?scl:"}

%install
rm -rf %{buildroot}
%{?scl:scl enable %{scl} "}
make pure_install DESTDIR=%{buildroot}
%{?scl:"}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
%{_fixperms} %{buildroot}

%check
%{?scl:scl enable %{scl} "}
make test
%{?scl:"}
%if 0%{?fedora} && 0%{!?perl_bootstrap:1} && ! ( 0%{?scl:1} )
%{?scl:scl enable %{scl} '}
make test TEST_FILES="xt/*/*.t"
%{?scl:'}
%endif

%clean
rm -rf %{buildroot}

%files
%doc Changes LICENSE README
%{perl_vendorlib}/CPAN/
%{_mandir}/man3/CPAN::Meta::YAML.3pm*

%changelog
* Tue Feb 11 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.010-3
- Fixed getting of *old_test_more
- Resolves: rhbz#1063206

* Tue Feb 04 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.010-2
- Disable release tests
- Resolves: rhbz#1061038, rhbz#1063206

* Tue Nov 12 2013 Jitka Plesnikova <jplesnik@redhat.com> - 0.010-1
- 0.010 bump
- Update dependencies

* Tue Jun 18 2013 Jitka Plesnikova <jplesnik@redhat.com> - 0.008-2
- Update a condition for BRs

* Tue Feb 12 2013 Jitka Plesnikova <jplesnik@redhat.com> - 0.008-1
- Stack package - initial release
