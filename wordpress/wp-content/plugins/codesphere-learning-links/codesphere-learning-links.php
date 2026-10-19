<?php
/**
 * Plugin Name: CodeSphere Learning Links
 * Plugin URI: https://github.com/codesphere/codesphere-learning-links
 * Description: Manages structured educational internal links (Prerequisites, Next Topics, Related Topics, Parent Hubs) to enforce contextual linking graphs and academic curriculum continuity.
 * Version: 1.0.0
 * Author: CodeSphere Engineering Team
 * License: MIT
 * Text Domain: codesphere-learning-links
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

if ( ! defined( 'CODESPHERE_LL_VERSION' ) ) {
    define( 'CODESPHERE_LL_VERSION', '1.0.0' );
}

if ( ! defined( 'CODESPHERE_LL_PATH' ) ) {
    define( 'CODESPHERE_LL_PATH', plugin_dir_path( __FILE__ ) );
}

require_once CODESPHERE_LL_PATH . 'includes/class-meta-box.php';
require_once CODESPHERE_LL_PATH . 'includes/class-schema.php';

/**
 * Initialize Plugin Components
 */
function codesphere_learning_links_init() {
    CodeSphere_Learning_Links_Meta_Box::init();
    CodeSphere_Learning_Links_Schema::init();
}
add_action( 'plugins_loaded', 'codesphere_learning_links_init' );

/**
 * Render structured learning system cards for a given post
 *
 * @param int $post_id Post ID to render links for.
 */
function codesphere_render_learning_system_links( $post_id = null ) {
    if ( ! $post_id ) {
        $post_id = get_the_ID();
    }

    $links_data = get_post_meta( $post_id, '_codesphere_learning_links', true );
    if ( empty( $links_data ) || ! is_array( $links_data ) ) {
        return;
    }

    // Filter to verify at least one category has valid links
    $has_links = false;
    foreach ( array( 'prerequisites', 'next_topics', 'related_topics', 'parent_hub' ) as $type ) {
        if ( ! empty( $links_data[ $type ] ) ) {
            $has_links = true;
            break;
        }
    }

    if ( ! $has_links ) {
        return;
    }

/**
 * Resolve an internal learning link URL to its active WordPress permalink.
 *
 * @param string $url Link URL from postmeta.
 * @return string Resolved URL.
 */
function codesphere_learning_links_resolve_url( $url ) {
    if ( empty( $url ) ) {
        return $url;
    }

    if ( preg_match( '#^https?://#i', $url ) ) {
        $home = home_url();
        if ( strpos( $url, $home ) === 0 ) {
            $rel = substr( $url, strlen( $home ) );
        } else {
            return $url;
        }
    } else {
        $rel = $url;
    }

    $trimmed = trim( $rel, '/' );
    $parts   = explode( '/', $trimmed );
    $clusters = array( 'programming', 'dsa', 'web-development', 'computer-science', 'blog' );

    if ( ! empty( $parts ) && in_array( $parts[0], $clusters, true ) && function_exists( 'codesphere_get_post_permalink' ) ) {
        $leaf = end( $parts );
        if ( ! empty( $leaf ) ) {
            return codesphere_get_post_permalink( $leaf, $url );
        }
    }

    if ( strpos( $url, '/' ) === 0 ) {
        return home_url( $url );
    }

    return $url;
}

    ?>
    <section class="learning-system-box" aria-labelledby="learning-pathways-heading">
        <h2 id="learning-pathways-heading" class="learning-system-title">
            <span aria-hidden="true">&#128218;</span> <?php esc_html_e( 'Curriculum Pathways & Related Concepts', 'codesphere-learning-links' ); ?>
        </h2>
        
        <div class="learning-link-grid">
            <?php
            // 1. Parent Hub Link
            if ( ! empty( $links_data['parent_hub'] ) ) :
                foreach ( $links_data['parent_hub'] as $item ) :
                    if ( empty( $item['url'] ) || empty( $item['title'] ) ) continue;
                    $item_url = codesphere_learning_links_resolve_url( $item['url'] );
                    ?>
                    <div class="learning-card">
                        <span class="learning-card-badge badge-hub"><?php esc_html_e( 'Parent Topic Hub', 'codesphere-learning-links' ); ?></span>
                        <a href="<?php echo esc_url( $item_url ); ?>" class="learning-card-title"><?php echo esc_html( $item['title'] ); ?></a>
                        <?php if ( ! empty( $item['description'] ) ) : ?>
                            <p class="learning-card-desc"><?php echo esc_html( $item['description'] ); ?></p>
                        <?php endif; ?>
                    </div>
                    <?php
                endforeach;
            endif;

            // 2. Prerequisites
            if ( ! empty( $links_data['prerequisites'] ) ) :
                foreach ( $links_data['prerequisites'] as $item ) :
                    if ( empty( $item['url'] ) || empty( $item['title'] ) ) continue;
                    $item_url = codesphere_learning_links_resolve_url( $item['url'] );
                    ?>
                    <div class="learning-card">
                        <span class="learning-card-badge badge-prereq"><?php esc_html_e( 'Prerequisite Concept', 'codesphere-learning-links' ); ?></span>
                        <a href="<?php echo esc_url( $item_url ); ?>" class="learning-card-title"><?php echo esc_html( $item['title'] ); ?></a>
                        <?php if ( ! empty( $item['description'] ) ) : ?>
                            <p class="learning-card-desc"><?php echo esc_html( $item['description'] ); ?></p>
                        <?php endif; ?>
                    </div>
                    <?php
                endforeach;
            endif;

            // 3. Next Topics
            if ( ! empty( $links_data['next_topics'] ) ) :
                foreach ( $links_data['next_topics'] as $item ) :
                    if ( empty( $item['url'] ) || empty( $item['title'] ) ) continue;
                    $item_url = codesphere_learning_links_resolve_url( $item['url'] );
                    ?>
                    <div class="learning-card">
                        <span class="learning-card-badge badge-next"><?php esc_html_e( 'Recommended Next', 'codesphere-learning-links' ); ?></span>
                        <a href="<?php echo esc_url( $item_url ); ?>" class="learning-card-title"><?php echo esc_html( $item['title'] ); ?></a>
                        <?php if ( ! empty( $item['description'] ) ) : ?>
                            <p class="learning-card-desc"><?php echo esc_html( $item['description'] ); ?></p>
                        <?php endif; ?>
                    </div>
                    <?php
                endforeach;
            endif;

            // 4. Related Topics
            if ( ! empty( $links_data['related_topics'] ) ) :
                foreach ( $links_data['related_topics'] as $item ) :
                    if ( empty( $item['url'] ) || empty( $item['title'] ) ) continue;
                    $item_url = codesphere_learning_links_resolve_url( $item['url'] );
                    ?>
                    <div class="learning-card">
                        <span class="learning-card-badge badge-related"><?php esc_html_e( 'Related Study', 'codesphere-learning-links' ); ?></span>
                        <a href="<?php echo esc_url( $item_url ); ?>" class="learning-card-title"><?php echo esc_html( $item['title'] ); ?></a>
                        <?php if ( ! empty( $item['description'] ) ) : ?>
                            <p class="learning-card-desc"><?php echo esc_html( $item['description'] ); ?></p>
                        <?php endif; ?>
                    </div>
                    <?php
                endforeach;
            endif;
            ?>
        </div>
    </section>
    <?php
}

/**
 * Register shortcode [codesphere_learning_links]
 */
function codesphere_learning_links_shortcode( $atts ) {
    ob_start();
    codesphere_render_learning_system_links();
    return ob_get_clean();
}
add_shortcode( 'codesphere_learning_links', 'codesphere_learning_links_shortcode' );
