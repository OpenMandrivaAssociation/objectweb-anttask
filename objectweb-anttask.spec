%define section         free
%define gcj_support     1

# -----------------------------------------------------------------------------

Summary:        ObjectWeb Ant task
Name:           objectweb-anttask
Version:        1.3.2
Release:        %mkrel 2
Epoch:		0
Group:          Development/Java
License:        LGPL
URL:            http://forge.objectweb.org/projects/monolog/
%if %{gcj_support}
Requires(post): java-gcj-compat
Requires(postun): java-gcj-compat
BuildRequires:  java-gcj-compat-devel
%else
BuildArch:      noarch
%endif
Source0:        http://download.fr2.forge.objectweb.org/monolog/ow_util_ant_tasks_%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
#Vendor:         JPackage Project
#Distribution:   JPackage
Requires:       asm2
BuildRequires:  java-devel
BuildRequires:  ant
# FIXME: This is a nice circular dependency.
BuildRequires:  asm2
BuildRequires:	jpackage-utils >= 0:1.5
Provides:	owanttask

%description
ObjectWeb Ant task

%prep
%setup -c -q -n %{name}
find . -name "*.class" -exec rm {} \;
find . -name "*.jar" -exec rm {} \;

%build
export CLASSPATH=$(build-classpath asm2)
export OPT_JAR_LIST=
%ant jar

%install
rm -rf $RPM_BUILD_ROOT

# jars
install -d -m 0755 $RPM_BUILD_ROOT%{_javadir}

install -m 644 output/lib/ow_util_ant_tasks.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
pushd $RPM_BUILD_ROOT%{_javadir}
  ln -sf %{name}-%{version}.jar %{name}.jar
popd

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
%{__rm} -rf %{buildroot}

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%{_javadir}/*
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*.jar.*
%endif

