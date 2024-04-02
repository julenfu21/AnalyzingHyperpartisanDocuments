from enum import Enum


class DocumentType(Enum):
    HYPERPARTISAN = "Hyperpartisan"
    NON_HYPERPARTISAN = "Non-Hyperpartisan"


class DataFileTypesNames(Enum):
    ARTICLES = "articles-validation-bypublisher-20181122"
    GROUND_TRUTH = "ground-truth-validation-bypublisher-20181122"
