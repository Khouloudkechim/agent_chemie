# GazOptim AI 

> Agent intelligent de décision énergétique pour la valorisation des gaz industriels de Gabès

---

## CONTEXTE & OBJECTIF

Tu es un ingénieur full-stack AI expert. Construis un projet complet et prêt pour la production appelé **"GazOptim AI"** — un agent intelligent de décision énergétique qui optimise la valorisation des gaz industriels de la région industrielle de Gabès en Tunisie.

Les industries de Gabès (phosphate, chimie, ciment) émettent divers gaz (CO, CH₄, H₂, SO₂, CO₂, N₂, H₂S) à la fois polluants et énergétiquement exploitables. GazOptim AI transforme ces émissions en source d'énergie utile (principalement de l'électricité) via une architecture d'agent IA combinant LangGraph, LangChain et un LLM via OpenRouter — sans dataset ML requis.

---

## STRUCTURE DU MONOREPO

```
gazoptim-ai/
├── web/                          # Frontend Next.js 14 (App Router)
├── backend/                      # Backend FastAPI architecture multi-services
├── others/                       # Assets, docs, configs de déploiement
│   ├── docker/
│   ├── docs/
│   └── scripts/
└── vibe/                         # Dossier vibe coding
    └── prompts/
```

---

## /backend — Architecture FastAPI Multi-Services

### Stack Technique
- Python 3.11+
- FastAPI + Uvicorn
- LangGraph (orchestration de l'agent)
- LangChain (outils, chaînes, mémoire)
- OpenRouter API (LLM : `mistralai/mistral-7b-instruct` par défaut)
- Pydantic v2
- Redis (cache d'état, optionnel)
- Server-Sent Events (SSE) pour le streaming temps réel

### Structure des Répertoires

```
backend/
├── main.py                        # Point d'entrée FastAPI
├── requirements.txt
├── .env.example
├── core/
│   ├── config.py                  # Settings (clé API OpenRouter, modèle, seuils)
│   └── constants.py               # Propriétés des gaz, constantes énergétiques, limites de sécurité
├── models/
│   ├── gas_input.py               # Pydantic : GasComposition, SensorReading
│   ├── decision.py                # Pydantic : EnergyDecision, enum DecisionType
│   └── report.py                  # Pydantic : AnalysisReport, SafetyAlert
├── services/
│   ├── gas_analyzer.py            # Calculs physiques/thermodynamiques
│   ├── energy_calculator.py       # Potentiel énergétique, estimation d'efficacité
│   ├── environmental_scorer.py    # Équivalent CO₂, indice de toxicité
│   ├── safety_checker.py          # Limites d'explosion, seuils de toxicité
│   └── decision_engine.py         # Pré-filtre basé sur règles avant le LLM
├── agent/
│   ├── graph.py                   # Définition du StateGraph LangGraph
│   ├── state.py                   # AgentState TypedDict
│   ├── nodes/
│   │   ├── analyze_node.py        # Nœud : analyse des gaz
│   │   ├── evaluate_node.py       # Nœud : évaluation énergie + environnement
│   │   ├── safety_node.py         # Nœud : vérification sécurité
│   │   ├── decision_node.py       # Nœud : prise de décision LLM
│   │   └── report_node.py         # Nœud : génération de rapport explicable
│   └── tools/
│       ├── gas_tools.py           # Outils LangChain pour calculs sur les gaz
│       ├── energy_tools.py        # Outils : valeur calorifique, rendement turbine
│       └── safety_tools.py        # Outils : vérification LEL/UEL, alerte H₂S
├── api/
│   ├── routes/
│   │   ├── analysis.py            # POST /api/analyze
│   │   ├── simulate.py            # POST /api/simulate
│   │   ├── stream.py              # GET /api/stream/{session_id} (SSE)
│   │   └── history.py             # GET /api/history
│   └── dependencies.py
└── utils/
    ├── llm_client.py              # Setup LLM OpenRouter via LangChain
    └── logger.py
```

---

### Logique Centrale à Implémenter

#### 1. Constantes Physiques des Gaz (`core/constants.py`)

Définir pour chaque gaz — CO, CH₄, H₂, SO₂, CO₂, H₂S, N₂, C₃H₈ :

| Propriété | Description | Unité |
|-----------|-------------|-------|
| `LHV` | Pouvoir calorifique inférieur | MJ/m³ |
| `gwp_factor` | Facteur d'équivalent CO₂ (PRG) | — |
| `LEL` | Limite inférieure d'explosivité | % vol. |
| `UEL` | Limite supérieure d'explosivité | % vol. |
| `tlv_twa` | Seuil de toxicité (valeur limite) | ppm |
| `combustion_temp` | Température de combustion | °C |
| `density_stp` | Densité aux conditions normales | kg/m³ |

#### 2. Agent LangGraph (`agent/graph.py`)

Construire un `StateGraph` avec ces nœuds et arêtes conditionnelles :

```
START
  → analyze_node         (extraire les fractions gazeuses, calculer les propriétés du mélange)
  → safety_node          (vérifier LEL, UEL, toxicité → si CRITICAL : arrêt d'urgence)
  → evaluate_node        (potentiel énergétique kWh/m³, score env., valeur économique)
  → decision_node        (appel LLM via OpenRouter avec contexte complet)
  → report_node          (générer un rapport structuré et explicable)
END

Arête conditionnelle depuis safety_node :
  - si safety_status == "CRITICAL" → report_node (contourner la décision, émettre une alerte)
  - sinon → evaluate_node
```

#### 3. AgentState (`agent/state.py`)

```python
class AgentState(TypedDict):
    session_id: str
    raw_input: GasComposition
    gas_analysis: dict           # propriétés physiques du mélange
    safety_status: str           # SAFE / WARNING / CRITICAL
    safety_alerts: list[str]
    energy_potential: float      # kWh/m³
    environmental_score: float   # 0–100 (plus bas = meilleur)
    economic_value: float        # EUR/1000m³ estimé
    llm_reasoning: str
    decision: DecisionType       # voir enum ci-dessous
    confidence: float
    recommendations: list[str]
    report: AnalysisReport
    errors: list[str]
```

#### 4. Types de Décision (Enum `DecisionType`)

| Valeur | Description |
|--------|-------------|
| `GENERATE_ELECTRICITY` | Combustion directe en turbine/moteur à gaz |
| `STORE` | Compression et stockage pour usage ultérieur |
| `CONVERT` | Reformage (production H₂) ou synthèse chimique |
| `FLARE_SAFELY` | Torchage contrôlé avec récupération d'énergie |
| `EMERGENCY_STOP` | Arrêt immédiat, alerte d'évacuation |

#### 5. Prompt du Nœud de Décision LLM (`decision_node.py`)

Le LLM reçoit un contexte structuré incluant :
- Composition du mélange gazeux (%)
- Potentiel énergétique calculé (kWh/m³)
- Statut de sécurité et alertes
- Score environnemental
- Estimation de la valeur économique
- Contraintes industrielles courantes

**Le LLM doit répondre en JSON :**

```json
{
  "decision": "GENERATE_ELECTRICITY",
  "confidence": 0.87,
  "reasoning": "Explication détaillée de la décision...",
  "recommendations": [
    "Recommandation 1...",
    "Recommandation 2..."
  ],
  "warnings": ["Avertissement éventuel..."]
}
```

#### 6. Endpoints API

| Méthode | Route | Description |
|---------|-------|-------------|
| `POST` | `/api/analyze` | Lance l'agent complet sur une composition gazeuse |
| `POST` | `/api/simulate` | Simule 3 scénarios industriels prédéfinis de Gabès |
| `GET` | `/api/stream/{session_id}` | SSE : diffuse les étapes d'exécution en temps réel |
| `GET` | `/api/health` | Vérification de l'état du service |

**Input `POST /api/analyze` :**
- Pourcentages de chaque gaz (GasComposition)
- Débit volumique (m³/h)
- Température (°C)
- Pression (bar)

**Scénarios prédéfinis `POST /api/simulate` :**
- `phosphate_plant` — GCT Gabès : SO₂ élevé, CO₂
- `cement_kiln` — CPG : CO élevé, CO₂
- `chemical_complex` — SIAPE : mélange SO₂, H₂S, CO₂

---

## /web — Frontend Next.js 14

### Stack Technique
- Next.js 14 (App Router)
- TypeScript
- Tailwind CSS + shadcn/ui
- Recharts (visualisation de données)
- Zustand (gestion d'état)
- React Hook Form + Zod (validation)
- Server-Sent Events (client SSE)

### Structure des Répertoires

```
web/
├── app/
│   ├── layout.tsx
│   ├── page.tsx                    # Dashboard principal
│   ├── analyze/
│   │   └── page.tsx                # Formulaire d'entrée gaz + analyse temps réel
│   ├── simulate/
│   │   └── page.tsx                # Simulateur de scénarios
│   ├── history/
│   │   └── page.tsx                # Historique des décisions
│   └── about/
│       └── page.tsx                # Infos projet, contexte Gabès
├── components/
│   ├── layout/
│   │   ├── Navbar.tsx
│   │   └── Sidebar.tsx
│   ├── dashboard/
│   │   ├── KPICards.tsx            # Potentiel énergie, score env., valeur éco.
│   │   ├── GasCompositionChart.tsx # Graphique camembert du mélange gazeux
│   │   ├── DecisionBadge.tsx       # Affichage de la décision avec code couleur
│   │   └── SafetyStatusBar.tsx     # Indicateur SAFE / WARNING / CRITICAL
│   ├── analyze/
│   │   ├── GasInputForm.tsx        # Formulaire avec sliders pour chaque gaz %
│   │   ├── AgentProgressStream.tsx # Affichage SSE des nœuds en temps réel
│   │   ├── ReportCard.tsx          # Rapport d'analyse complet
│   │   └── RecommendationsList.tsx
│   ├── simulate/
│   │   ├── ScenarioSelector.tsx    # Sélecteur des 3 scénarios Gabès
│   │   └── ComparisonTable.tsx     # Tableau comparatif + radar chart
│   └── shared/
│       ├── LoadingSpinner.tsx
│       └── AlertBanner.tsx
├── lib/
│   ├── api.ts                      # Fonctions client API
│   ├── sse.ts                      # Gestionnaire de flux SSE
│   └── types.ts                    # Types TypeScript partagés
├── store/
│   └── analysisStore.ts            # Store Zustand
└── public/
    └── gabes-map.svg               # Illustration carte industrielle de Gabès
```

### Fonctionnalités UI Clés à Construire

#### 1. Dashboard
- Cartes KPI affichant en temps réel : potentiel énergétique (kWh/m³), score environnemental, valeur économique estimée
- Placeholder de carte de la région de Gabès
- Graphique d'historique des décisions récentes

#### 2. Formulaire d'Entrée des Gaz
- Sliders interactifs (0–100%) pour chaque gaz : CO, CH₄, H₂, SO₂, CO₂, H₂S, N₂
- Validation temps réel : somme des pourcentages = 100%
- Champs pour débit (m³/h), température (°C), pression (bar)

#### 3. Flux de Progression de l'Agent (SSE)
Stepper vertical affichant chaque nœud LangGraph avec statut (en attente / en cours / terminé) :

```
🔬 Analyse de la composition gazeuse...
🛡️ Vérification des paramètres de sécurité...
⚡ Évaluation du potentiel énergétique...
🤖 Prise de décision par l'IA...
📊 Génération du rapport...
```

#### 4. Affichage de la Décision
Grand badge avec code couleur :

| Décision | Couleur |
|----------|---------|
| 🟢 GENERATE_ELECTRICITY | Vert |
| 🔵 STORE | Bleu |
| 🟡 CONVERT | Jaune |
| 🟠 FLARE_SAFELY | Orange |
| 🔴 EMERGENCY_STOP | Rouge |

#### 5. Rapport Explicable
- Raisonnement LLM affiché en texte clair
- Barre de confiance (0–100%)
- Liste de recommandations ordonnées
- Alertes de sécurité mises en évidence

#### 6. Simulateur de Scénarios
- Comparaison des 3 scénarios Gabès côte à côte
- Radar chart (énergie / environnement / sécurité / économie)

---

## /others — Assets & Déploiement

```
others/
├── docker/
│   ├── docker-compose.yml          # Stack complète : web + backend + redis
│   ├── Dockerfile.backend
│   └── Dockerfile.web
├── docs/
│   ├── architecture.md
│   ├── gas_constants_reference.md
│   └── gabes_industrial_context.md
└── scripts/
    ├── seed_scenarios.py            # Pré-populate les 3 scénarios Gabès
    └── test_agent.py                # Test d'intégration de l'agent
```

**Services docker-compose.yml :**
- `web` → port 3000
- `backend` → port 8000
- `redis` → port 6379

---

## /vibe — Vibe Coding

```
vibe/
└── prompts/
    ├── agent_design.md
    ├── ui_components.md
    └── gas_physics.md
```

---

## EXIGENCES D'IMPLÉMENTATION

### Comportements Obligatoires

#### 1. Précision Physique
Tous les calculs énergétiques doivent utiliser de vraies constantes thermodynamiques (PCI, équations de combustion). Le calcul du potentiel énergétique doit tenir compte de la composition du mélange et du rendement de combustion (~35% pour une turbine à gaz).

#### 2. Sécurité en Premier
Le nœud de sécurité doit TOUJOURS s'exécuter avant le nœud de décision.

| Condition | Action |
|-----------|--------|
| H₂S > 10 ppm | WARNING |
| H₂S > 50 ppm | CRITICAL → EMERGENCY_STOP |
| LEL > 20% | CRITICAL → EMERGENCY_STOP |

#### 3. Explicabilité
Chaque décision doit inclure le raisonnement étape par étape du LLM. Le rapport doit être lisible par un opérateur industriel non expert.

#### 4. Contexte Gabès
Inclure des scénarios réalistes basés sur les industries réelles de Gabès :

| ID Scénario | Industrie | Composition Typique |
|-------------|-----------|---------------------|
| `phosphate_plant` | GCT (Groupe Chimique Tunisien) | SO₂ élevé, CO₂ |
| `cement_kiln` | CPG (Ciment) | CO élevé, CO₂ |
| `chemical_complex` | SIAPE (Engrais) | SO₂, H₂S, CO₂ mixte |

#### 5. Setup LLM OpenRouter

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=settings.OPENROUTER_API_KEY,
    model="mistralai/mistral-7b-instruct",
    temperature=0.1,
)
```

#### 6. Variables d'Environnement (`.env`)

```env
OPENROUTER_API_KEY=your_key_here
OPENROUTER_MODEL=mistralai/mistral-7b-instruct
BACKEND_URL=http://localhost:8000
REDIS_URL=redis://localhost:6379
```

### Standards de Qualité du Code

- Annotations de types complètes (Python + TypeScript)
- Modèles Pydantic v2 pour toutes les structures de données
- Gestion des erreurs à chaque nœud avec dégradation gracieuse
- Logging au niveau INFO pour toutes les étapes de l'agent
- CORS configuré : `localhost:3000` ↔ `localhost:8000`

---

## ORDRE D'IMPLÉMENTATION

Commence par créer la structure complète du monorepo, puis implémente dans cet ordre :

1. `backend/core/constants.py` — constantes physiques des gaz
2. `backend/agent/state.py` — définition de l'AgentState
3. `backend/agent/graph.py` — squelette du graphe LangGraph
4. `backend/agent/nodes/` — les 5 nœuds de l'agent
5. `backend/services/` — calculateurs physiques
6. `backend/agent/tools/` — outils LangChain
7. `backend/api/routes/` — endpoints FastAPI
8. `backend/main.py` — assemblage de l'application
9. `web/` — application Next.js complète
10. `others/docker/` — docker-compose et Dockerfiles

---

## FLUX DE DONNÉES COMPLET

```
[Opérateur industriel]
        │
        ▼
[Formulaire Web — composition gazeuse + paramètres]
        │
        ▼
[POST /api/analyze]
        │
        ▼
[LangGraph Agent]
   ├── analyze_node    → calcule propriétés du mélange
   ├── safety_node     → LEL/UEL/toxicité → SAFE/WARNING/CRITICAL
   ├── evaluate_node   → kWh/m³, score env., valeur éco.
   ├── decision_node   → LLM OpenRouter → JSON décision
   └── report_node     → rapport structuré explicable
        │
        ▼ (SSE stream en parallèle)
[Frontend — affichage temps réel]
   ├── Stepper de progression des nœuds
   ├── Badge de décision coloré
   ├── Rapport complet avec raisonnement LLM
   └── Alertes de sécurité si nécessaire
```

---

*GazOptim AI — Transforming industrial emissions into intelligent energy decisions for a sustainable Gabès.*
