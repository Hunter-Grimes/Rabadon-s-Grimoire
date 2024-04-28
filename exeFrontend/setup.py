from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {'packages': ["os", "asyncio", "PySide6", "requests", "willump"], 'excludes': [], 'include_files': ['dragontailData', 'CommunityDragon', 'loading.gif', 'pipInfo.json', 'tabStyle.qss']}

base = 'gui'

executables = [
    Executable('main.py', base=base, target_name = 'Rabadonsgrimoire', icon='RG.icns')
]

setup(name="RabadonsGrimoire",
      version = '1.0',
      description = 'version 1',
      options = {'build_exe': build_options},
      executables = executables)
