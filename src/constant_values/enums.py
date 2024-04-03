from enum import Enum


class DocumentType(Enum):
    HYPERPARTISAN = "hyperpartisan"
    NON_HYPERPARTISAN = "non-hyperpartisan"


class DataFileTypesNames(Enum):
    ARTICLES = "articles-validation-bypublisher-20181122"
    GROUND_TRUTH = "ground-truth-validation-bypublisher-20181122"


class TokenType(Enum):
    UNIGRAM = "unigram"
    BIGRAM = "bigram"
