# System Architecture

```mermaid
flowchart TD
    User["Human reviewer / operator"] --> CLI["run_affix.py generate"]

    CLI --> AffixCLI["src/affix/cli.py"]
    AffixCLI --> Loaders["loaders.py<br/>Read input CSV"]
    AffixCLI --> Generator["generator.py<br/>Generate article ideas"]
    AffixCLI --> Writers["writer.py<br/>Write outputs"]
    AffixCLI --> Logger["logger.py<br/>Append operation logs"]

    Niches["data/input/niches.csv<br/>Niche candidates"] --> Loaders
    Keywords["data/input/keywords.csv<br/>Keyword candidates"] --> Loaders

    Loaders --> Models["models.py<br/>Niche / Keyword / ArticleIdea"]
    Models --> Generator

    Generator --> ArticleIdeas["Article ideas<br/>review-first structured data"]

    ArticleIdeas --> Writers
    Writers --> JSON["data/output/article_ideas.json"]
    Writers --> CSV["data/output/article_ideas.csv"]
    Writers --> Drafts["content/drafts/*.md<br/>Markdown review drafts"]

    Logger --> Assumptions["logs/assumptions.md"]
    Logger --> Progress["logs/progress.md"]
    Logger --> Risks["logs/risks.md"]
    Logger --> NextActions["logs/next_actions.md"]

    Drafts --> User
    JSON --> FutureAutomation["Future automation"]
    CSV --> FutureAutomation

    FutureAutomation -. explicit approval required .-> WordPress["WordPress draft publishing"]
    FutureAutomation -. explicit approval required .-> StaticSite["Static site export"]
    FutureAutomation -. scheduled checks .-> GitHubActions["GitHub Actions"]

    AGENTS["AGENTS.md<br/>Autonomous work rules"] -. guides .-> AffixCLI
    Config[".codex/config.toml<br/>Safe local policy notes"] -. constrains .-> AffixCLI

    classDef input fill:#eef7ff,stroke:#4b8bbe,color:#111;
    classDef code fill:#f5f5f5,stroke:#777,color:#111;
    classDef output fill:#f0fff4,stroke:#4c9a62,color:#111;
    classDef log fill:#fff8e6,stroke:#b58b00,color:#111;
    classDef future fill:#f8f0ff,stroke:#8a5cc2,color:#111;
    classDef safety fill:#fff0f0,stroke:#cc6666,color:#111;

    class Niches,Keywords input;
    class CLI,AffixCLI,Loaders,Generator,Writers,Logger,Models code;
    class JSON,CSV,Drafts,ArticleIdeas output;
    class Assumptions,Progress,Risks,NextActions log;
    class FutureAutomation,WordPress,StaticSite,GitHubActions future;
    class AGENTS,Config,User safety;
```

## Notes

- Current automation stops at review-ready article idea and Markdown draft generation.
- Publishing integrations are intentionally future components and require explicit human approval.
- Generated content is treated as draft material until facts, affiliate disclosure, and YMYL risks are reviewed.
