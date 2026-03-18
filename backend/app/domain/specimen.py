"""試験片データのドメイン型."""

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray


@dataclass
class SpecimenData:
    """試験片の応力ひずみデータ.

    Attributes:
        name: 試験片名
        strain: ひずみ配列（無次元）
        stress: 応力配列（MPa）
        raw_strain: 元のひずみ配列（単位変換前）
        raw_stress: 元の応力配列（単位変換前）
    """

    name: str
    strain: NDArray[np.float64]
    stress: NDArray[np.float64]
    raw_strain: NDArray[np.float64] | None = None
    raw_stress: NDArray[np.float64] | None = None

    def __post_init__(self) -> None:
        """データの整合性を検証."""
        assert len(self.strain) == len(self.stress), (
            f"strain ({len(self.strain)}) and stress ({len(self.stress)}) "
            "must have the same length"
        )
        assert len(self.strain) > 0, "Data must not be empty"
