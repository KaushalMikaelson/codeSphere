<?php
/**
 * Page Template for CodeSphere
 *
 * @package CodeSphere
 */

get_header();

while ( have_posts() ) :
    the_post();
    ?>
    <article id="post-<?php the_ID(); ?>" <?php post_class( 'page-article' ); ?>>
        <header class="page-header" style="margin-bottom: 2rem;">
            <h1 class="page-title" style="margin-top: 0;"><?php the_title(); ?></h1>
        </header>

        <div class="content-layout-two-col">
            <div class="article-main">
                <div class="entry-content">
                    <?php the_content(); ?>
                </div>

                <?php
                if ( function_exists( 'codesphere_render_learning_system_links' ) ) {
                    codesphere_render_learning_system_links( get_the_ID() );
                }
                ?>
            </div>

            <aside class="sidebar-wrapper" aria-label="<?php esc_attr_e( 'Page Navigation', 'codesphere' ); ?>">
                <div class="toc-sidebar">
                    <h2 class="toc-title"><?php esc_html_e( 'Page Sections', 'codesphere' ); ?></h2>
                    <ul class="toc-list">
                        <!-- Filled by main.js if headings exist -->
                    </ul>
                </div>
            </aside>
        </div>
    </article>
    <?php
endwhile;

get_footer();
