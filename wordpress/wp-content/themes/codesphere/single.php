<?php
/**
 * Single Article Template for CodeSphere
 *
 * @package CodeSphere
 */

get_header();

while ( have_posts() ) :
    the_post();
    ?>
    <article id="post-<?php the_ID(); ?>" <?php post_class( 'article-container' ); ?>>
        <header class="article-header" style="margin-bottom: 2rem;">
            <div style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 0.5rem; text-transform: uppercase; font-weight: 600;">
                <?php
                $categories = get_the_category();
                if ( ! empty( $categories ) ) {
                    echo '<a href="' . esc_url( get_category_link( $categories[0]->term_id ) ) . '">' . esc_html( $categories[0]->name ) . '</a>';
                }
                ?>
                &bull; <?php echo esc_html( codesphere_reading_time() ); ?> <?php esc_html_e( 'min read', 'codesphere' ); ?>
            </div>
            <h1 class="article-title" style="margin-top: 0;"><?php the_title(); ?></h1>
            <div style="font-size: 0.9rem; color: var(--text-muted);">
                <?php esc_html_e( 'Last updated: ', 'codesphere' ); ?><time datetime="<?php echo esc_attr( get_the_modified_date( 'c' ) ); ?>"><?php echo esc_html( get_the_modified_date( 'F j, Y' ) ); ?></time>
            </div>
        </header>

        <div class="content-layout-two-col">
            <div class="article-main">
                <div class="entry-content">
                    <?php the_content(); ?>
                </div>

                <!-- Structured Learning Path & Internal Links Hook -->
                <?php
                if ( function_exists( 'codesphere_render_learning_system_links' ) ) {
                    codesphere_render_learning_system_links( get_the_ID() );
                }
                ?>

                <!-- Previous / Next Topic Navigation -->
                <nav class="post-navigation-split" aria-label="<?php esc_attr_e( 'Topic sequence navigation', 'codesphere' ); ?>">
                    <?php
                    $prev_post = get_previous_post();
                    if ( $prev_post ) :
                        ?>
                        <a href="<?php echo esc_url( get_permalink( $prev_post->ID ) ); ?>" class="nav-previous-card">
                            <span class="nav-card-label">&larr; <?php esc_html_e( 'Previous Topic', 'codesphere' ); ?></span>
                            <span class="nav-card-title"><?php echo esc_html( get_the_title( $prev_post->ID ) ); ?></span>
                        </a>
                    <?php else : ?>
                        <div></div>
                    <?php endif; ?>

                    <?php
                    $next_post = get_next_post();
                    if ( $next_post ) :
                        ?>
                        <a href="<?php echo esc_url( get_permalink( $next_post->ID ) ); ?>" class="nav-next-card">
                            <span class="nav-card-label"><?php esc_html_e( 'Next Topic', 'codesphere' ); ?> &rarr;</span>
                            <span class="nav-card-title"><?php echo esc_html( get_the_title( $next_post->ID ) ); ?></span>
                        </a>
                    <?php endif; ?>
                </nav>
            </div>

            <!-- Sticky Sidebar with Table of Contents -->
            <aside class="sidebar-wrapper" aria-label="<?php esc_attr_e( 'Article outline', 'codesphere' ); ?>">
                <div class="toc-sidebar">
                    <h2 class="toc-title"><?php esc_html_e( 'Table of Contents', 'codesphere' ); ?></h2>
                    <ul class="toc-list">
                        <!-- Populated dynamically via Vanilla JS -->
                    </ul>
                </div>
            </aside>
        </div>
    </article>
    <?php
endwhile;

get_footer();
