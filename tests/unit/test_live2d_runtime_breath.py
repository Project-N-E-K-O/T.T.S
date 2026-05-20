import json
import shutil
import subprocess
from pathlib import Path

import pytest


LIVE2D_MODEL_PATH = Path(__file__).resolve().parents[2] / "static" / "live2d-model.js"


def _run_live2d_runtime_breath_scenario(script_body: str) -> dict:
    node_executable = shutil.which("node")
    if node_executable is None:
        pytest.skip("node not found")

    node_harness = f"""
const fs = require('fs');
const vm = require('vm');

global.window = global;
global.requestAnimationFrame = function (callback) {{
  return setTimeout(callback, 0);
}};
global.cancelAnimationFrame = function (id) {{
  clearTimeout(id);
}};
global.console = {{
  log() {{}},
  warn() {{}},
  error(...args) {{
    process.stderr.write(args.join(' ') + '\\n');
  }},
}};
global.Live2DManager = function Live2DManager() {{
  this.currentModel = null;
  this.savedModelParameters = null;
  this._shouldApplySavedParams = false;
  this._autoEyeBlinkEnabled = false;
  this._eyeBlinkParams = null;
  this._temporaryPoseOverrides = new Map();
  this._temporaryPoseOverride = null;
  this._mouthOverrideInstalled = false;
  this._origMotionManagerUpdate = null;
  this._origCoreModelUpdate = null;
  this._coreModelRef = null;
  this._runtimeBreathTime = 0;
  this._runtimeBreathParamIds = null;
}};

global.Live2DManager.prototype._isEyeBlinkParamId = function () {{
  return false;
}};
global.Live2DManager.prototype.isAvatarPerformanceCapabilityLocked = function () {{
  return false;
}};
global.Live2DManager.prototype.getPersistentExpressionParamIds = function () {{
  return new Set();
}};
global.Live2DManager.prototype._scheduleReinstallOverride = function () {{}};
global.Live2DManager.prototype._updateRandomLookAt = function () {{}};
global.Live2DManager.prototype._updateEyeBlink = function () {{}};
global.Live2DManager.prototype._applyTemporaryPoseOverride = function () {{}};
global.LIPSYNC_PARAMS = ['ParamMouthOpenY', 'ParamMouthForm'];

function createCoreModel(initialValues = {{}}) {{
  const ids = ['ParamBreath', 'ParamBreath2', 'ParamMouthOpenY', 'ParamMouthForm'];
  const values = new Map(ids.map((id) => [id, initialValues[id] ?? 0]));
  const indexById = new Map(ids.map((id, index) => [id, index]));
  const idByIndex = ids.slice();
  return {{
    writes: [],
    getParameterIndex(id) {{
      return indexById.has(id) ? indexById.get(id) : -1;
    }},
    getParameterValueByIndex(index) {{
      return values.get(idByIndex[index]) ?? 0;
    }},
    getParameterValueById(id) {{
      return values.get(id) ?? 0;
    }},
    setParameterValueByIndex(index, value) {{
      const id = idByIndex[index];
      values.set(id, value);
      this.writes.push({{ id, value }});
    }},
    setParameterValueById(id, value) {{
      values.set(id, value);
      this.writes.push({{ id, value }});
    }},
    getParameterMinimumValueByIndex(index) {{
      return idByIndex[index] === 'ParamBreath' ? 0 : 0;
    }},
    getParameterMaximumValueByIndex(index) {{
      return idByIndex[index] === 'ParamBreath' ? 1 : 1;
    }},
    getParameterDefaultValueByIndex() {{
      return 0;
    }},
  }};
}}

function createManager(coreModel, motionUpdate) {{
  const manager = new Live2DManager();
  const motionManager = {{
    update: motionUpdate || function () {{}},
  }};
  manager.currentModel = {{
    deltaTime: 16.66,
    internalModel: {{
      coreModel,
      motionManager,
    }},
  }};
  return {{ manager, motionManager }};
}}

const source = fs.readFileSync({json.dumps(str(LIVE2D_MODEL_PATH))}, 'utf8');
vm.runInThisContext(source, {{ filename: {json.dumps(str(LIVE2D_MODEL_PATH))} }});

function runScenario() {{
{script_body}
}}

try {{
  const result = runScenario();
  process.stdout.write(JSON.stringify(result));
}} catch (error) {{
  process.stderr.write(String(error && error.stack ? error.stack : error));
  process.exit(1);
}}
"""

    result = subprocess.run(
        [node_executable, "-"],
        input=node_harness,
        text=True,
        capture_output=True,
        check=False,
        timeout=10,
    )

    if result.returncode != 0:
        raise AssertionError(
            "Node live2d runtime breath scenario failed:\n"
            f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        )

    return json.loads(result.stdout)


@pytest.mark.unit
def test_runtime_breath_fallback_animates_param_breath():
    result = _run_live2d_runtime_breath_scenario(
        """
  const coreModel = createCoreModel();
  const { manager } = createManager(coreModel);

  manager._updateRuntimeBreath(0.25);
  const first = coreModel.getParameterValueById('ParamBreath');
  manager._updateRuntimeBreath(0.25);
  const second = coreModel.getParameterValueById('ParamBreath');

  return {
    first,
    second,
    writeCount: coreModel.writes.filter((entry) => entry.id === 'ParamBreath').length,
  };
"""
    )

    assert 0 < result["first"] < 1
    assert 0 < result["second"] < 1
    assert result["first"] != result["second"]
    assert result["writeCount"] == 2


@pytest.mark.unit
def test_motion_manager_update_applies_runtime_breath_when_motion_is_static():
    result = _run_live2d_runtime_breath_scenario(
        """
  const coreModel = createCoreModel();
  const { manager, motionManager } = createManager(coreModel);

  manager.installMouthOverride();
  motionManager.update();

  return {
    breathValue: coreModel.getParameterValueById('ParamBreath'),
    isBreathDrivenByMotion: manager._isBreathDrivenByMotion,
  };
"""
    )

    assert result["breathValue"] > 0
    assert result["isBreathDrivenByMotion"] is False


@pytest.mark.unit
def test_motion_manager_update_does_not_override_motion_driven_breath():
    result = _run_live2d_runtime_breath_scenario(
        """
  const coreModel = createCoreModel();
  const { manager, motionManager } = createManager(coreModel, function () {
    const idx = coreModel.getParameterIndex('ParamBreath');
    coreModel.setParameterValueByIndex(idx, 0.25);
  });

  manager.installMouthOverride();
  motionManager.update();

  return {
    breathValue: coreModel.getParameterValueById('ParamBreath'),
    isBreathDrivenByMotion: manager._isBreathDrivenByMotion,
    breathWrites: coreModel.writes.filter((entry) => entry.id === 'ParamBreath').map((entry) => entry.value),
  };
"""
    )

    assert result["breathValue"] == pytest.approx(0.25)
    assert result["isBreathDrivenByMotion"] is True
    assert result["breathWrites"] == [pytest.approx(0.25)]
