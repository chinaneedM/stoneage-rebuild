# Presentation Engine Requirements Audit R1

Date: 2026-09-30

## Status

**CLOSED EVALUATION AUDIT.** No production renderer is bound by this document.

This audit evaluates presentation engines only after the deterministic local runtime obtained a stable semantic boundary:

`runtime stack -> session coordinator -> local application facade -> semantic engine adapter`

The engine is therefore treated as a replaceable presentation/input implementation, not as authority for world state, collision, persistence or recovered transition rules.

## 1. Project requirements

The first presentation implementation must support:

1. strong native 2D sprite/tile/animation workflows suitable for a classic top-down RPG;
2. Windows desktop development and packaging;
3. a thin adapter around the existing deterministic semantic command/update contract;
4. local save-path integration without taking ownership of save schema semantics;
5. practical animation, UI and audio tooling for a content-heavy single-player game;
6. efficient iteration for a small team / solo-directed project;
7. long-term maintainability and reasonable dependency autonomy;
8. custom data import paths for reconstructed maps/NPCs/items without requiring legacy StoneAge file formats at runtime;
9. no dependency on MMO account/network services;
10. room for a future authorized client/server split without changing deterministic game rules.

The audit does **not** reward 3D features, multiplayer services, cloud backends or asset-store breadth unless they materially help this project.

## 2. Evidence snapshot

### Godot

- Current stable line observed on 2026-09-30: **Godot 4.7.2-stable**, released 2026-08-18.
- Godot documents a dedicated 2D renderer/physics/tooling stack including tile maps, sprites, animation, lighting and particles.
- Windows is a supported editor/export platform; both Standard and .NET builds are published.
- The engine is MIT licensed; games remain separately licensable.
- .NET builds provide C# support in addition to GDScript/GDExtension.

Official references:

- https://godotengine.org/article/maintenance-release-godot-4-7-2/
- https://godotengine.org/download/archive/4.7.2-stable/
- https://docs.godotengine.org/en/stable/tutorials/2d/introduction_to_2d.html
- https://godotengine.org/license/

### Unity

- **Unity 6.3 LTS** is the current long-term-support line and is documented as supported through December 2027.
- Unity provides mature 2D Sprite, Tilemap and 2D Animation tooling plus Windows standalone targets.
- Unity Personal remains free in 2026 for users/organizations under the published USD 200,000 revenue/funding threshold; higher tiers are proprietary paid products.
- C# is the native scripting/application language surface.

Official references:

- https://docs.unity.com/en-us/engine/6000.7/manual/whats-new/unity63
- https://unity.com/releases/editor/archive
- https://unity.com/products/pricing-updates
- https://docs.unity3d.com/ja/current/Manual/com.unity.2d.sprite.html
- https://docs.unity3d.com/cn/current/ScriptReference/BuildTarget.StandaloneWindows64.html

### Defold

- The current 1.13 line is actively maintained; **1.13.2** was announced on 2026-09-29 after 1.13.1.
- Defold is a lightweight turnkey engine/editor with explicit 2D workflows, Tile Map, sprite/flipbook animation and Windows bundling.
- Defold is free to use under the Defold License, which permits commercial games, extensions and modified engine distributions subject to that license.
- Runtime scripting centers on Lua; native extensions are available where required.

Official references:

- https://forum.defold.com/t/defold-1-13-2-has-been-released/83276
- https://defold.com/manuals/introduction/
- https://defold.com/manuals/tilemap/
- https://defold.com/manuals/sprite/
- https://defold.com/manuals/bundling/
- https://defold.com/license/

### MonoGame

- Current released maintenance version observed: **MonoGame 3.8.5.1**, released 2026-08-14.
- MonoGame supports Windows and other desktop/mobile/console targets and includes an extensible content pipeline.
- Its own documentation explicitly describes MonoGame as a “bring your own tools” framework, **not** a scene-editor game engine.
- This gives high control and a C#-native code surface, but shifts scene, map, UI and workflow tooling onto the project.

Official references:

- https://monogame.net/blog/2026-08-14-3.8.5.1-release-2026/
- https://docs.monogame.net/articles/index.html
- https://docs.monogame.net/articles/getting_started/
- https://docs.monogame.net/articles/getting_to_know/whatis/content_pipeline/CP_Architecture.html

## 3. Project-fit matrix

| Requirement | Godot 4.7.2 | Unity 6.3 LTS | Defold 1.13.x | MonoGame 3.8.5.1 |
| --- | --- | --- | --- | --- |
| First-class 2D editor/tooling | Strong | Strong | Strong/lightweight | Weak by design; bring your own tools |
| Tile/sprite/animation workflow | Native and broad | Native and broad | Native and compact | Framework/content-pipeline primitives |
| Windows desktop packaging | Native | Native | Native | Native |
| Thin semantic adapter possible | Yes | Yes | Yes | Yes |
| C# route | Godot .NET | Native | Not primary | Native |
| License/autonomy | MIT, strongest fit | Proprietary product terms | Free custom license | Open-source framework |
| Editor/tooling burden | Low | Low-medium | Low | High |
| Runtime footprint/complexity | Moderate | Higher | Low | Low-medium, but project code grows |
| Fit for custom recovered data | Strong via custom import/tool scripts | Strong via editor tooling | Strong, but Lua/native bridge work | Strong code-level control; more tooling to build |
| Long-term project independence | High | Medium | High-medium | High |
| Immediate fit for this project | **Primary spike candidate** | Mature fallback | Lightweight secondary candidate | Control baseline, not first presentation choice |

## 4. Decision

### Primary presentation spike candidate: Godot 4.7.2

Godot best matches the current project boundary because:

- the game is fundamentally 2D and content-heavy;
- dedicated 2D tools reduce the amount of editor/tooling we must build ourselves;
- Windows export is first-class;
- MIT licensing aligns with a private, long-lived reconstruction whose future legal/distribution status must remain flexible;
- the .NET build gives a credible C# path if the production deterministic core is later moved out of Python;
- the engine can remain behind the already-defined semantic adapter instead of becoming the source of game truth.

This is a **spike priority**, not yet a production lock-in.

### Secondary candidate: Defold

Defold is technically attractive for a small 2D game and has a compact toolchain. Its main project-specific cost is language/runtime divergence: the current deterministic reference implementation is Python, while Defold's normal runtime surface is Lua. A production port or native-extension boundary would still be required.

### Unity fallback

Unity has ample 2D tooling and strong C# support. It remains a technically capable fallback, especially if future requirements demand its ecosystem. For this project, the larger proprietary/editor footprint and changing commercial plan surface provide less long-term autonomy than Godot while adding little that the current reconstructed 2D runtime actually needs.

### MonoGame control baseline

MonoGame offers maximal code-level control and a direct C# environment, but its own documentation is explicit that it is not a scene-editor engine. For a reconstruction with hundreds of maps and a large future NPC/pet/item content surface, choosing it first would deliberately take on editor and content-tool work that Godot/Unity/Defold already provide.

## 5. Critical unresolved issue before an engine spike

The current recovered runtime implementation is Python and is serving both as executable specification and reconstruction infrastructure.

None of the candidate engine choices makes “ship the current Python modules unchanged inside the game” an obviously desirable production architecture.

Therefore the next decision is **not** “start drawing in Godot.” It is to close the production runtime language/hosting boundary:

- decide which Python modules remain research/reference tooling only;
- decide whether deterministic production rules are ported to a standalone C# core, GDScript, Lua, or another host;
- preserve parity with the Python reference through versioned golden fixtures;
- avoid embedding a Python interpreter merely to preserve implementation convenience unless a measured prototype proves that path materially superior.

Until that boundary is closed, Godot remains the preferred presentation **spike candidate**, not a production dependency.
