cmake_minimum_required(VERSION 3.20)
if(NOT DEFINED PSXRECOMP_ROOT)
    if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/psxrecomp/runtime/runtime.cmake")
        set(PSXRECOMP_ROOT "${CMAKE_CURRENT_SOURCE_DIR}/psxrecomp" CACHE PATH "Path to psxrecomp")
    elseif(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/../psxrecomp/runtime/runtime.cmake")
        set(PSXRECOMP_ROOT "${CMAKE_CURRENT_SOURCE_DIR}/../psxrecomp" CACHE PATH "Path to psxrecomp")
    else()
        message(FATAL_ERROR "PSXRecomp runtime is missing. Expected in psxrecomp/ or ../psxrecomp/")
    endif()
endif()

project(FinalFantasy8Recomp LANGUAGES C CXX)

set(PSX_SETUP_WIZARD ON CACHE BOOL
    "Advertise first-run setup wizard + Generate & rebuild in recomp-ui" FORCE)
set(PSX_GL_BATCH_IMPL "HLE" CACHE STRING "OpenGL textured batching" FORCE)
include("${PSXRECOMP_ROOT}/runtime/runtime.cmake")

set(PSX_PRELOADED_MODS "${CMAKE_CURRENT_SOURCE_DIR}/mods/preloaded")
if(NOT IS_DIRECTORY "${PSX_PRELOADED_MODS}")
    set(PSX_PRELOADED_MODS "NONE")
endif()

psxrecomp_add_game_runtime(psx-runtime
    PRELOADED_MODS_DIR "${PSX_PRELOADED_MODS}"
    ENABLE_SETUP_WIZARD
    WINDOW_TITLE "Final Fantasy VIII Recompiled"
    DEFAULT_GAME_CONFIG_PATH "game.toml"
    MAX_PLAYERS 1
    APP_ICON "${PSXRECOMP_ROOT}/assets/psxrecomp.ico"
    GEN_MARKER "generated/SLES_020.84_dispatch.c"
    GEN_FULL_GLOB "generated/SLES_020.84_full_*.c"
    CODEGEN_SETUP_SOURCES "${CMAKE_CURRENT_SOURCE_DIR}/codegen_setup.c"
)

foreach(_PSX_RUNTIME_CONFIG game.toml game_options.toml)
    if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/${_PSX_RUNTIME_CONFIG}")
        add_custom_command(TARGET psx-runtime POST_BUILD
            COMMAND ${CMAKE_COMMAND} -E copy_if_different
                "${CMAKE_CURRENT_SOURCE_DIR}/${_PSX_RUNTIME_CONFIG}"
                "$<TARGET_FILE_DIR:psx-runtime>/${_PSX_RUNTIME_CONFIG}"
            COMMENT "Staging ${_PSX_RUNTIME_CONFIG}"
            VERBATIM)
    endif()
endforeach()
