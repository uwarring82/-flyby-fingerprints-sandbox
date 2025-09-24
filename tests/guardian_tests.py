from __future__ import annotations

"""Guardian validation tests for background modelling utilities."""

import numpy as np

from simulations.background_effects import (
    BackgroundComponent,
    boulder_nist_2006_emi_patterns,
    detector_dead_time_effects,
    electromagnetic_pickup_models,
    innsbruck_2010_surface_signatures,
    surface_patch_potential_drift,
    vacuum_system_transients,
)
from simulations.null_validation import (
    BackgroundDataset,
    false_positive_rate_validation,
    generate_background_only_datasets,
    statistical_power_analysis,
)


def _flatten_catalogue() -> tuple[BackgroundComponent, ...]:
    groups = (
        electromagnetic_pickup_models(),
        vacuum_system_transients(),
        detector_dead_time_effects(),
        surface_patch_potential_drift(),
        boulder_nist_2006_emi_patterns(),
        innsbruck_2010_surface_signatures(),
    )
    components: list[BackgroundComponent] = []
    for group in groups:
        components.extend(group)
    return tuple(components)


def test_background_components_have_metadata() -> None:
    components = _flatten_catalogue()
    assert components, "Guardian catalogue must not be empty"
    for component in components:
        assert isinstance(component, BackgroundComponent)
        assert component.name
        assert component.references
        assert component.notes
        assert component.sigma > 0
        rng1 = np.random.default_rng(5)
        rng2 = np.random.default_rng(5)
        samples1 = component.sample(rng1, size=8)
        samples2 = component.sample(rng2, size=8)
        assert samples1.shape == (8,)
        assert np.allclose(samples1, samples2)


def test_generate_background_only_datasets_structure() -> None:
    components = _flatten_catalogue()
    datasets = generate_background_only_datasets(
        num_runs=2, n_samples=128, rng_seed=123
    )
    assert len(datasets) == 2
    for dataset in datasets:
        assert isinstance(dataset, BackgroundDataset)
        assert dataset.data.shape == (128, len(components))
        assert dataset.component_names == tuple(component.name for component in components)
        summary = dataset.summary()
        assert summary["n_samples"] == 128
        assert summary["n_components"] == len(components)


def test_power_and_false_positive_metrics_are_reasonable() -> None:
    datasets = generate_background_only_datasets(
        num_runs=3, n_samples=256, rng_seed=77
    )
    power = statistical_power_analysis(
        datasets, injection_strength=0.6, detection_threshold=2.0
    )
    assert 0.0 <= power["mean_power"] <= 1.0
    assert len(power["per_dataset"]) == len(datasets)
    assert power["mean_power"] > 0.5

    false_positives = false_positive_rate_validation(
        datasets, detection_threshold=3.0
    )
    assert 0.0 <= false_positives["rate"] <= 1.0
    assert len(false_positives["per_dataset"]) == len(datasets)
    assert false_positives["rate"] < 0.1
