---
issue: 3
---

# Issue #3 — Cherry-pick ROS 2 improvements from closed PR #1

## Integrated Review
**Status**: complete
**When**: 2026-09-11 09:05 -04:00
**By**: Claude Code Agent (Claude Opus 5 (1M context))

**PR**: #4 at `a59144e`
**Sources**: 1 (Copilot R1 @ `5a84f40`, Copilot R2 @ `a59144e`; no prior local timeline — legacy PR predates progress.md)
**Cross-source confirmations**: 0
**CI**: all-pass, but the four checks are the Copilot agent workflow (Prepare / Agent / Upload results / Cleanup artifacts) — this repo has no build or test CI

### Findings
- [ ] (must-fix, Copilot R2) `drixNumber` is declared with no default, so launching without it aborts — verified: `RuntimeError: Required launch argument "drixNumber" was not provided`. `display_launch.py` declares `default_value='8'`; the other two do not. Fix: match it — `launch/load_launch.py`, `launch/publish_state_launch.py`
- [ ] (must-fix, Copilot R1) Fixed Frame is `/project11/drix_8/base_link` with a leading slash; the xacro emits `project11/drix_8/base_link` and ROS 2 tf2 rejects leading-slash frame ids, so RViz resolves no frame. Fix: drop the slash — `config/drix_8.rviz`
- [ ] (should-fix, Copilot R2) `display_launch.py` runs rviz2 but `rviz2` is not an `exec_depend`, so a rosdep/binary install need not pull it in. Fix: add the dependency — `package.xml`
- [ ] (should-fix, Copilot R1+R2) The RViz config path is hard-coded to `config/drix_8.rviz` while `drixNumber` is parameterized, so any other hull number loads drix_8's TF tree and topics. Fix: add an `rviz_config` launch argument defaulting to the current file, or derive the name from `drixNumber` — `launch/display_launch.py`
- [ ] (decision, Copilot R1) The same commit began installing `models/` and deleted the `GZ_SIM_RESOURCE_PATH` environment hook, so nothing can discover the model. Mitigating: `models/` holds only `model.config` and a README placeholder — `drix.dae` does not exist and the xacro uses placeholder box/cylinder geometry. Decide: restore the hook, or stop installing `models/` until meshes land — `CMakeLists.txt`
- [ ] (low, Copilot R2) All three launch files pass `drixNumber:=` into xacro, but `urdf/drix_mesh.xacro` declares only `namespace`. Verified on Jazzy: xacro exits 0 and silently ignores the undeclared arg, so the claimed error cannot occur here — but the argument is dead plumbing. Fix: remove the three occurrences — `launch/*.py`

### False positives
- (Copilot R1) `config/drix_8.rviz` line 59 — claimed nothing publishes `/project11/drix_8/robot_description`, so RobotModel would receive no description. robot_state_publisher publishes the URDF on its namespaced `robot_description` topic with transient-local durability (Jazzy `robot_state_publisher.hpp`: "publishes the text of the URDF to the network on the /robot_description topic"), and all three launch files start it in exactly that namespace. The topic is published; the display resolves.
