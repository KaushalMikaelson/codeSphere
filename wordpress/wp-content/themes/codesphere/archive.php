<?php
/**
 * Archive & Category Cluster Template for CodeSphere
 *
 * @package CodeSphere
 */

get_header();
?>

<header class="archive-header" style="margin-bottom: 2.5rem; border-bottom: 2px solid var(--border-color); padding-bottom: 1.5rem;">
    <span class="learning-card-badge badge-hub" style="margin-bottom: 0.5rem; display: inline-block;">
        <?php esc_html_e( 'Cluster Index', 'codesphere' ); ?>
    </span>
    <h1 class="archive-title" style="margin: 0.25rem 0;">
        <?php the_archive_title(); ?>
    </h1>
    <?php
    $description = get_the_archive_description();
    if ( $description ) {
        echo '<div class="archive-description" style="color: var(--text-secondary); max-width: 750px; font-size: 1.1rem; margin-top: 0.5rem;">' . wp_kses_post( $description ) . '</div>';
    }
    ?>
</header>

<div class="learning-link-grid" style="grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));">
    <?php
    if ( have_posts() ) :
        while ( have_posts() ) :
            the_post();
            ?>
            <article class="learning-card">
                <span class="learning-card-badge badge-related"><?php esc_html_e( 'Curriculum Article', 'codesphere' ); ?></span>
                <h2 style="font-size: 1.25rem; margin: 0.35rem 0;">
                    <a href="<?php the_permalink(); ?>" class="learning-card-title"><?php the_title(); ?></a>
                </h2>
                <div class="learning-card-desc">
                    <?php echo wp_trim_words( get_the_excerpt(), 25, '...' ); ?>
                </div>
                <div style="margin-top: auto; padding-top: 1rem; font-size: 0.85rem; color: var(--accent-primary); font-weight: 600;">
                    <a href="<?php the_permalink(); ?>"><?php esc_html_e( 'Read Guide &rarr;', 'codesphere' ); ?></a>
                </div>
            </article>
            <?php
        endwhile;

        the_posts_navigation();
    else :
        ?>
        <p><?php esc_html_e( 'No educational topics found in this category yet.', 'codesphere' ); ?></p>
        <?php
    endif;
    ?>
</div>

<?php
get_footer();
