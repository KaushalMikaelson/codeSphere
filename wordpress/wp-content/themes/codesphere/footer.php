<?php
/**
 * Footer Template for CodeSphere
 *
 * @package CodeSphere
 */
?>
    </div><!-- /.site-container -->
</main><!-- /#primary-content -->

<footer class="site-footer" role="contentinfo">
    <div class="site-container">
        <div class="footer-grid">
            <div>
                <h3 class="footer-heading"><?php esc_html_e( 'CodeSphere Knowledge Base', 'codesphere' ); ?></h3>
                <p style="font-size:0.9rem; max-width:320px;">
                    <?php esc_html_e( 'An interlinked computer science curriculum designed for undergraduate engineering students and technical interview preparation.', 'codesphere' ); ?>
                </p>
                <p style="font-size:0.8rem; color:var(--text-muted);">
                    <?php esc_html_e( 'Academic research project evaluating internal-link topologies, crawl efficiency, and PageRank distribution.', 'codesphere' ); ?>
                </p>
            </div>

            <div>
                <h4 class="footer-heading"><?php esc_html_e( 'Programming & DSA', 'codesphere' ); ?></h4>
                <ul class="footer-links">
                    <li><a href="<?php echo esc_url( codesphere_get_post_permalink( 'programming-fundamentals', '/programming/programming-fundamentals/' ) ); ?>"><?php esc_html_e( 'Programming Fundamentals', 'codesphere' ); ?></a></li>
                    <li><a href="<?php echo esc_url( codesphere_get_post_permalink( 'object-oriented-programming', '/programming/object-oriented-programming/' ) ); ?>"><?php esc_html_e( 'Object-Oriented Programming', 'codesphere' ); ?></a></li>
                    <li><a href="<?php echo esc_url( codesphere_get_post_permalink( 'data-structures', '/dsa/data-structures/' ) ); ?>"><?php esc_html_e( 'Data Structures Hub', 'codesphere' ); ?></a></li>
                    <li><a href="<?php echo esc_url( codesphere_get_post_permalink( 'binary-trees', '/dsa/trees/binary-trees/' ) ); ?>"><?php esc_html_e( 'Binary Trees', 'codesphere' ); ?></a></li>
                    <li><a href="<?php echo esc_url( codesphere_get_post_permalink( 'recursion', '/dsa/algorithms/recursion/' ) ); ?>"><?php esc_html_e( 'Recursion & Backtracking', 'codesphere' ); ?></a></li>
                </ul>
            </div>

            <div>
                <h4 class="footer-heading"><?php esc_html_e( 'Web & Systems', 'codesphere' ); ?></h4>
                <ul class="footer-links">
                    <li><a href="<?php echo esc_url( codesphere_get_post_permalink( 'rest-apis', '/web-development/rest-apis/' ) ); ?>"><?php esc_html_e( 'REST APIs Architecture', 'codesphere' ); ?></a></li>
                    <li><a href="<?php echo esc_url( codesphere_get_post_permalink( 'backend-fundamentals', '/web-development/backend-fundamentals/' ) ); ?>"><?php esc_html_e( 'Backend Fundamentals', 'codesphere' ); ?></a></li>
                    <li><a href="<?php echo esc_url( codesphere_get_post_permalink( 'databases', '/computer-science/databases/' ) ); ?>"><?php esc_html_e( 'Databases Hub (SQL vs NoSQL)', 'codesphere' ); ?></a></li>
                    <li><a href="<?php echo esc_url( codesphere_get_post_permalink( 'computer-networks', '/computer-science/computer-networks/' ) ); ?>"><?php esc_html_e( 'Computer Networks Basics', 'codesphere' ); ?></a></li>
                    <li><a href="<?php echo esc_url( codesphere_get_post_permalink( 'operating-systems', '/computer-science/operating-systems/' ) ); ?>"><?php esc_html_e( 'Operating Systems Concepts', 'codesphere' ); ?></a></li>
                </ul>
            </div>

            <div>
                <h4 class="footer-heading"><?php esc_html_e( 'Research & Sitemap', 'codesphere' ); ?></h4>
                <ul class="footer-links">
                    <li><a href="<?php echo esc_url( codesphere_get_post_permalink( 'about', '/about/' ) ); ?>"><?php esc_html_e( 'About CodeSphere', 'codesphere' ); ?></a></li>
                    <li><a href="<?php echo esc_url( codesphere_get_post_permalink( 'dsa-roadmap-for-placements', '/blog/dsa-roadmap-for-placements/' ) ); ?>"><?php esc_html_e( 'DSA Roadmap for Placements', 'codesphere' ); ?></a></li>
                    <li><a href="<?php echo esc_url( codesphere_get_post_permalink( 'binary-tree-vs-binary-search-tree', '/blog/binary-tree-vs-binary-search-tree/' ) ); ?>"><?php esc_html_e( 'Binary Tree vs BST Guide', 'codesphere' ); ?></a></li>
                    <li><a href="<?php echo esc_url( home_url( '/sitemap.xml' ) ); ?>" rel="nofollow"><?php esc_html_e( 'XML Sitemap', 'codesphere' ); ?></a></li>
                    <li><a href="<?php echo esc_url( home_url( '/robots.txt' ) ); ?>" rel="nofollow"><?php esc_html_e( 'Robots.txt', 'codesphere' ); ?></a></li>
                </ul>
            </div>
        </div>

        <div class="footer-bottom">
            <div>
                &copy; <?php echo esc_html( date( 'Y' ) ); ?> <?php bloginfo( 'name' ); ?>. <?php esc_html_e( 'Released for educational & academic research purposes.', 'codesphere' ); ?>
            </div>
            <div>
                <?php esc_html_e( 'Fast, crawlable, accessible architecture.', 'codesphere' ); ?>
            </div>
        </div>
    </div>
</footer>

<?php wp_footer(); ?>
</body>
</html>
