# CodeSphere Academic Research Methodology & Graph Modeling

**Subject:** Empirical Internal-Link Graph Analysis and Information Architecture in Computer Science Education  
**Project Lead:** CodeSphere Engineering Team  
**Institution Context:** Undergraduate B.Tech / B.E. Computer Science Engineering Curriculum  

---

## 1. Central Research Question & Objectives

> **Central Research Question:**  
> *“Can a deliberately designed internal-link structure improve page discoverability, reduce click depth, eliminate orphan pages, and improve connectivity between related learning topics?”*

### Core Hypotheses:
1. **$H_1$ (Discoverability & Orphan Elimination):** Introducing semantic curriculum connections (Prerequisites, Next Topics, Hubs) will eliminate orphan articles from the published inventory without resorting to site-wide menu bloat.
2. **$H_2$ (Click Depth Reduction):** Direct contextual transitions between foundational concepts (e.g., Recursion) and dependent advanced topics (e.g., Dynamic Programming) will reduce maximum crawl distance from the homepage.
3. **$H_3$ (Link Equity & Trapping Mitigation):** Establishing reciprocal pathways will reduce dead-end pages ($d_{out} = 0$), promoting continuous crawl equity circulation modeled via PageRank.

---

## 2. Mathematical Graph Formulation

The website is formally represented as a directed graph:
$$G = (V, E)$$
Where:
- $V$: Set of unique, normalized internal HTML pages (vertices).
- $E \subseteq V \times V$: Set of ordered pairs $(u, v)$ representing unique hyperlinks pointing from source page $u$ to target page $v$. Parallel hyperlinks between the same page pair are deduplicated.

### Topological Metrics Formulations:

1. **In-Degree ($d_{in}(v)$):**
   $$d_{in}(v) = |\{u \in V : (u, v) \in E\}|$$
   Represents the total number of distinct internal pages referencing topic $v$.

2. **Out-Degree ($d_{out}(u)$):**
   $$d_{out}(u) = |\{v \in V : (u, v) \in E\}|$$
   Represents the outbound navigational pathways originating from page $u$. A node where $d_{out}(u) = 0$ is classified as a **Dead-End**.

3. **Shortest Click Depth ($\delta(root, v)$):**
   $$\delta(root, v) = \min \{ \text{length}(p) : p \text{ is a directed path from } root \text{ to } v \text{ in } G \}$$
   If no directed path exists, $\delta(root, v) = \infty$ (recorded as $-1$ in export tables).

4. **Orphan Page Identification:**
   A published URL $v \in V_{\text{inventory}}$ is defined as an **Orphan Page** if and only if:
   $$d_{in}(v) = 0 \quad \lor \quad \delta(root, v) = \infty$$

5. **Internal PageRank Formulation:**
   Using the classic Brin and Page formulation implemented via NetworkX:
   $$PR(u) = \frac{1 - \alpha}{|V|} + \alpha \sum_{v \in M(u)} \frac{PR(v)}{d_{out}(v)}$$
   Where:
   - $M(u)$: Set of pages linking to $u$.
   - $\alpha = 0.85$: Standard damping factor representing the probability that a random reader continues following links rather than jumping to a random page.
   - Max iterations: $100$; convergence tolerance: $10^{-6}$.

---

## 3. Academic Disclaimers & Ethics

1. **Internal PageRank is NOT Google Ranking:**  
   Google’s live search engine ranking systems (incorporating RankBrain, BERT, MUM, spam classifiers, and hundreds of signals) do not correlate 1:1 with isolated internal PageRank. In this study, PageRank serves strictly as an objective, mathematical metric of relative graph centrality and link equity circulation within a closed network.
2. **No Guaranteed Organic Rankings:**  
   Deliberate internal linking structures streamline crawler discovery, improve user navigation, and eliminate crawl waste, but external authority, domain history, user intent fulfillment, and search indexing policies ultimately govern SERP outcomes.
