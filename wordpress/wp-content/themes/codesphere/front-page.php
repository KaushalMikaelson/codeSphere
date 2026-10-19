<?php
/**
 * Front Page Template for CodeSphere
 *
 * @package CodeSphere
 */

get_header();
?>

<section class="hero-section">
    <span class="hero-badge"><?php esc_html_e( 'Academic CS Knowledge Base & Research', 'codesphere' ); ?></span>
    <h1 class="hero-title"><?php esc_html_e( 'Master Core Computer Science with Structured Learning Paths', 'codesphere' ); ?></h1>
    <p class="hero-description">
        <?php esc_html_e( 'An interlinked educational curriculum built for undergraduate engineering students. Designed to teach programming, data structures, algorithms, system architecture, and placement roadmaps through crawlable, contextual knowledge graphs.', 'codesphere' ); ?>
    </p>
</section>

<section class="clusters-section" aria-label="<?php esc_attr_e( 'Topic Clusters', 'codesphere' ); ?>">
    <h2 style="text-align: center; border-bottom: none; margin-bottom: 2rem;">
        <?php esc_html_e( 'Explore the Four Core Knowledge Clusters', 'codesphere' ); ?>
    </h2>

    <div class="clusters-grid">
        <!-- Cluster 1: Programming -->
        <div class="cluster-card cluster-card-prog">
            <h3 class="cluster-card-title"><?php esc_html_e( 'Programming Fundamentals', 'codesphere' ); ?></h3>
            <p><?php esc_html_e( 'Core language mechanics, data types, control structures, and object-oriented principles.', 'codesphere' ); ?></p>
            <ul class="cluster-card-links">
                <li><a href="<?php echo esc_url( codesphere_get_post_permalink( 'programming-fundamentals', '/programming/programming-fundamentals/' ) ); ?>">&rarr; <?php esc_html_e( 'Programming Fundamentals Hub', 'codesphere' ); ?></a></li>
                <li><a href="<?php echo esc_url( codesphere_get_post_permalink( 'variables-data-types', '/programming/variables-data-types/' ) ); ?>">&rarr; <?php esc_html_e( 'Variables & Data Types', 'codesphere' ); ?></a></li>
                <li><a href="<?php echo esc_url( codesphere_get_post_permalink( 'control-flow', '/programming/control-flow/' ) ); ?>">&rarr; <?php esc_html_e( 'Control Flow & Logic', 'codesphere' ); ?></a></li>
                <li><a href="<?php echo esc_url( codesphere_get_post_permalink( 'functions', '/programming/functions/' ) ); ?>">&rarr; <?php esc_html_e( 'Functions & Modular Design', 'codesphere' ); ?></a></li>
                <li><a href="<?php echo esc_url( codesphere_get_post_permalink( 'object-oriented-programming', '/programming/object-oriented-programming/' ) ); ?>">&rarr; <?php esc_html_e( 'OOP Concepts & Patterns', 'codesphere' ); ?></a></li>
            </ul>
        </div>

        <!-- Cluster 2: Data Structures & Algorithms -->
        <div class="cluster-card cluster-card-dsa">
            <h3 class="cluster-card-title"><?php esc_html_e( 'Data Structures & Algorithms', 'codesphere' ); ?></h3>
            <p><?php esc_html_e( 'Linear structures, hierarchical tree models, dynamic programming, and complexity analysis.', 'codesphere' ); ?></p>
            <ul class="cluster-card-links">
                <li><a href="<?php echo esc_url( codesphere_get_post_permalink( 'data-structures', '/dsa/data-structures/' ) ); ?>">&rarr; <?php esc_html_e( 'Data Structures Hub', 'codesphere' ); ?></a></li>
                <li><a href="<?php echo esc_url( codesphere_get_post_permalink( 'arrays', '/dsa/arrays/' ) ); ?>">&rarr; <?php esc_html_e( 'Arrays & Memory Contiguity', 'codesphere' ); ?></a></li>
                <li><a href="<?php echo esc_url( codesphere_get_post_permalink( 'linked-lists', '/dsa/linked-lists/' ) ); ?>">&rarr; <?php esc_html_e( 'Singly & Doubly Linked Lists', 'codesphere' ); ?></a></li>
                <li><a href="<?php echo esc_url( codesphere_get_post_permalink( 'stacks-and-queues', '/dsa/stacks-and-queues/' ) ); ?>">&rarr; <?php esc_html_e( 'Stacks & Queues', 'codesphere' ); ?></a></li>
                <li><a href="<?php echo esc_url( codesphere_get_post_permalink( 'binary-trees', '/dsa/trees/binary-trees/' ) ); ?>">&rarr; <?php esc_html_e( 'Binary Trees Architecture', 'codesphere' ); ?></a></li>
                <li><a href="<?php echo esc_url( codesphere_get_post_permalink( 'binary-search-trees', '/dsa/trees/binary-search-trees/' ) ); ?>">&rarr; <?php esc_html_e( 'Binary Search Trees (BST)', 'codesphere' ); ?></a></li>
                <li><a href="<?php echo esc_url( codesphere_get_post_permalink( 'tree-traversal', '/dsa/trees/tree-traversal/' ) ); ?>">&rarr; <?php esc_html_e( 'Tree Traversal (In/Pre/Post)', 'codesphere' ); ?></a></li>
                <li><a href="<?php echo esc_url( codesphere_get_post_permalink( 'recursion', '/dsa/algorithms/recursion/' ) ); ?>">&rarr; <?php esc_html_e( 'Recursion Fundamentals', 'codesphere' ); ?></a></li>
                <li><a href="<?php echo esc_url( codesphere_get_post_permalink( 'dynamic-programming', '/dsa/algorithms/dynamic-programming/' ) ); ?>">&rarr; <?php esc_html_e( 'Dynamic Programming (DP)', 'codesphere' ); ?></a></li>
            </ul>
        </div>

        <!-- Cluster 3: Web Development -->
        <div class="cluster-card cluster-card-web">
            <h3 class="cluster-card-title"><?php esc_html_e( 'Web Development', 'codesphere' ); ?></h3>
            <p><?php esc_html_e( 'Client-server communications, semantic HTML, modern styling, and scalable REST APIs.', 'codesphere' ); ?></p>
            <ul class="cluster-card-links">
                <li><a href="<?php echo esc_url( codesphere_get_post_permalink( 'html', '/web-development/html/' ) ); ?>">&rarr; <?php esc_html_e( 'Semantic HTML5 & Accessibility', 'codesphere' ); ?></a></li>
                <li><a href="<?php echo esc_url( codesphere_get_post_permalink( 'css', '/web-development/css/' ) ); ?>">&rarr; <?php esc_html_e( 'CSS3 Layouts, Flexbox & Grid', 'codesphere' ); ?></a></li>
                <li><a href="<?php echo esc_url( codesphere_get_post_permalink( 'javascript', '/web-development/javascript/' ) ); ?>">&rarr; <?php esc_html_e( 'JavaScript Engine & Async Event Loop', 'codesphere' ); ?></a></li>
                <li><a href="<?php echo esc_url( codesphere_get_post_permalink( 'rest-apis', '/web-development/rest-apis/' ) ); ?>">&rarr; <?php esc_html_e( 'RESTful API Design & HTTP', 'codesphere' ); ?></a></li>
                <li><a href="<?php echo esc_url( codesphere_get_post_permalink( 'backend-fundamentals', '/web-development/backend-fundamentals/' ) ); ?>">&rarr; <?php esc_html_e( 'Backend Architecture & Servers', 'codesphere' ); ?></a></li>
            </ul>
        </div>

        <!-- Cluster 4: Core Computer Science -->
        <div class="cluster-card cluster-card-cs">
            <h3 class="cluster-card-title"><?php esc_html_e( 'Core Computer Science', 'codesphere' ); ?></h3>
            <p><?php esc_html_e( 'Relational and document storage, networking protocols, and operating system kernels.', 'codesphere' ); ?></p>
            <ul class="cluster-card-links">
                <li><a href="<?php echo esc_url( codesphere_get_post_permalink( 'databases', '/computer-science/databases/' ) ); ?>">&rarr; <?php esc_html_e( 'Database Systems Hub', 'codesphere' ); ?></a></li>
                <li><a href="<?php echo esc_url( codesphere_get_post_permalink( 'sql', '/computer-science/sql/' ) ); ?>">&rarr; <?php esc_html_e( 'SQL Queries & Normalization', 'codesphere' ); ?></a></li>
                <li><a href="<?php echo esc_url( codesphere_get_post_permalink( 'nosql', '/computer-science/nosql/' ) ); ?>">&rarr; <?php esc_html_e( 'NoSQL Models & CAP Theorem', 'codesphere' ); ?></a></li>
                <li><a href="<?php echo esc_url( codesphere_get_post_permalink( 'computer-networks', '/computer-science/computer-networks/' ) ); ?>">&rarr; <?php esc_html_e( 'Computer Networks & OSI Stack', 'codesphere' ); ?></a></li>
                <li><a href="<?php echo esc_url( codesphere_get_post_permalink( 'operating-systems', '/computer-science/operating-systems/' ) ); ?>">&rarr; <?php esc_html_e( 'Operating Systems & Concurrency', 'codesphere' ); ?></a></li>
            </ul>
        </div>
    </div>
</section>

<!-- Placement Roadmaps & Comparative Guides Section -->
<section style="margin-top: 3.5rem; background: var(--bg-secondary); border: 1px solid var(--border-color); border-radius: var(--radius-lg); padding: 2rem;">
    <h2 style="margin-top: 0;"><?php esc_html_e( 'Placement Guides & Comparative Engineering Studies', 'codesphere' ); ?></h2>
    <p><?php esc_html_e( 'In-depth articles designed to synthesize concepts across multiple clusters to prepare students for technical interviews and viva examinations.', 'codesphere' ); ?></p>
    
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.5rem; margin-top: 1.5rem;">
        <div style="background: var(--bg-card); padding: 1.25rem; border-radius: var(--radius-md); border: 1px solid var(--border-color);">
            <span class="learning-card-badge badge-prereq"><?php esc_html_e( 'Career Roadmap', 'codesphere' ); ?></span>
            <h3 style="font-size: 1.15rem; margin: 0.5rem 0;"><a href="<?php echo esc_url( codesphere_get_post_permalink( 'dsa-roadmap-for-placements', '/blog/dsa-roadmap-for-placements/' ) ); ?>"><?php esc_html_e( 'Complete DSA Roadmap for Campus Placements', 'codesphere' ); ?></a></h3>
            <p style="font-size: 0.9rem; margin-bottom: 0;"><?php esc_html_e( 'A semester-by-semester milestone guide covering array fundamentals to advanced dynamic programming and graph theory.', 'codesphere' ); ?></p>
        </div>
        <div style="background: var(--bg-card); padding: 1.25rem; border-radius: var(--radius-md); border: 1px solid var(--border-color);">
            <span class="learning-card-badge badge-related"><?php esc_html_e( 'Comparative Study', 'codesphere' ); ?></span>
            <h3 style="font-size: 1.15rem; margin: 0.5rem 0;"><a href="<?php echo esc_url( codesphere_get_post_permalink( 'binary-tree-vs-binary-search-tree', '/blog/binary-tree-vs-binary-search-tree/' ) ); ?>"><?php esc_html_e( 'Binary Tree vs Binary Search Tree: In-Depth Comparison', 'codesphere' ); ?></a></h3>
            <p style="font-size: 0.9rem; margin-bottom: 0;"><?php esc_html_e( 'Structural differences, search complexity (O(N) vs O(log N)), traversal mechanics, and interview questions.', 'codesphere' ); ?></p>
        </div>
    </div>
</section>

<?php
get_footer();
