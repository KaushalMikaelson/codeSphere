<?php
/**
 * Main Fallback Template for CodeSphere
 *
 * @package CodeSphere
 */

get_header();
?>

<div class="site-container">
    <header class="page-header" style="margin-bottom: 2rem;">
        <h1 class="page-title"><?php esc_html_e( 'Computer Science Curriculum Index', 'codesphere' ); ?></h1>
    </header>

    <div class="learning-link-grid">
        <?php
        if ( have_posts() ) :
            while ( have_posts() ) :
                the_post();
                ?>
                <article class="learning-card">
                    <h2 class="learning-card-title">
                        <a href="<?php the_permalink(); ?>"><?php the_title(); ?></a>
                    </h2>
                    <div class="learning-card-desc">
                        <?php the_excerpt(); ?>
                    </div>
                </article>
                <?php
            endwhile;

            the_posts_navigation();
        else :
            ?>
            <p><?php esc_html_e( 'No content available.', 'codesphere' ); ?></p>
            <?php
        endif;
        ?>
    </div>
</div>

<?php
get_footer();
