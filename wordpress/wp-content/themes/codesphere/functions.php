<?php
/**
 * CodeSphere Theme Functions & Definitions
 *
 * @package CodeSphere
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit; // Exit if accessed directly
}

/**
 * Sets up theme defaults and registers support for various WordPress features.
 */
function codesphere_setup() {
    // Make theme available for translation
    load_theme_textdomain( 'codesphere', get_template_directory() . '/languages' );

    // Add default posts and comments RSS feed links to head
    add_theme_support( 'automatic-feed-links' );

    // Let WordPress manage the document title
    add_theme_support( 'title-tag' );

    // Enable support for Post Thumbnails
    add_theme_support( 'post-thumbnails' );

    // Switch default core markup to output valid HTML5
    add_theme_support( 'html5', array(
        'search-form',
        'comment-form',
        'comment-list',
        'gallery',
        'caption',
        'style',
        'script',
        'navigation-widgets',
    ) );

    // Register navigation menus
    register_nav_menus( array(
        'primary' => esc_html__( 'Primary Navigation (Clusters)', 'codesphere' ),
        'footer'  => esc_html__( 'Footer Cluster Links', 'codesphere' ),
    ) );
}
add_action( 'after_setup_theme', 'codesphere_setup' );

/**
 * Enqueue scripts and styles.
 */
function codesphere_scripts() {
    // Google Fonts (Inter & JetBrains Mono)
    wp_enqueue_style(
        'codesphere-fonts',
        'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap',
        array(),
        null
    );

    // Theme main stylesheet
    wp_enqueue_style( 'codesphere-style', get_stylesheet_uri(), array(), '1.0.0' );
    wp_enqueue_style( 'codesphere-components', get_template_directory_uri() . '/assets/css/main.css', array( 'codesphere-style' ), '1.0.0' );

    // Vanilla JS
    wp_enqueue_script( 'codesphere-scripts', get_template_directory_uri() . '/assets/js/main.js', array(), '1.0.0', true );
}
add_action( 'wp_enqueue_scripts', 'codesphere_scripts' );

/**
 * Breadcrumb Generator for Academic / Educational Hierarchies
 */
function codesphere_breadcrumbs() {
    if ( is_front_page() ) {
        return;
    }

    echo '<nav class="breadcrumbs-nav" aria-label="' . esc_attr__( 'Breadcrumbs', 'codesphere' ) . '">';
    echo '<ol itemscope itemtype="https://schema.org/BreadcrumbList">';

    // Home item
    echo '<li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">';
    echo '<a itemprop="item" href="' . esc_url( home_url( '/' ) ) . '"><span itemprop="name">' . esc_html__( 'Home', 'codesphere' ) . '</span></a>';
    echo '<meta itemprop="position" content="1" />';
    echo '</li>';

    $position = 2;

    if ( is_single() ) {
        // Topic category or parent cluster
        $categories = get_the_category();
        if ( ! empty( $categories ) ) {
            $cat = $categories[0];
            echo '<li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">';
            echo '<a itemprop="item" href="' . esc_url( get_category_link( $cat->term_id ) ) . '"><span itemprop="name">' . esc_html( $cat->name ) . '</span></a>';
            echo '<meta itemprop="position" content="' . $position . '" />';
            echo '</li>';
            $position++;
        }
        // Current post title
        echo '<li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">';
        echo '<span itemprop="name" aria-current="page">' . esc_html( get_the_title() ) . '</span>';
        echo '<meta itemprop="position" content="' . $position . '" />';
        echo '</li>';
    } elseif ( is_page() ) {
        global $post;
        if ( $post->post_parent ) {
            $ancestors = array_reverse( get_post_ancestors( $post->ID ) );
            foreach ( $ancestors as $ancestor ) {
                echo '<li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">';
                echo '<a itemprop="item" href="' . esc_url( get_permalink( $ancestor ) ) . '"><span itemprop="name">' . esc_html( get_the_title( $ancestor ) ) . '</span></a>';
                echo '<meta itemprop="position" content="' . $position . '" />';
                echo '</li>';
                $position++;
            }
        }
        echo '<li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">';
        echo '<span itemprop="name" aria-current="page">' . esc_html( get_the_title() ) . '</span>';
        echo '<meta itemprop="position" content="' . $position . '" />';
        echo '</li>';
    } elseif ( is_category() ) {
        echo '<li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">';
        echo '<span itemprop="name" aria-current="page">' . esc_html( single_cat_title( '', false ) ) . '</span>';
        echo '<meta itemprop="position" content="' . $position . '" />';
        echo '</li>';
    }

    echo '</ol>';
    echo '</nav>';
}

/**
 * Estimate reading time in minutes
 */
function codesphere_reading_time() {
    $content = get_post_field( 'post_content', get_the_ID() );
    $word_count = str_word_count( strip_tags( $content ) );
    $reading_time = ceil( $word_count / 200 );
    return max( 1, $reading_time );
}

/**
 * Output TechArticle structured data in head for Single Posts
 */
function codesphere_output_schema() {
    if ( ! is_single() ) {
        return;
    }

    $post_id = get_the_ID();
    $schema = array(
        '@context'         => 'https://schema.org',
        '@type'            => 'TechArticle',
        'headline'         => get_the_title(),
        'url'              => get_permalink(),
        'datePublished'    => get_the_date( 'c' ),
        'dateModified'     => get_the_modified_date( 'c' ),
        'mainEntityOfPage' => array(
            '@type' => 'WebPage',
            '@id'   => get_permalink(),
        ),
        'publisher'        => array(
            '@type' => 'Organization',
            'name'  => get_bloginfo( 'name' ),
            'url'   => home_url(),
        ),
        'inLanguage'       => 'en',
        'proficiencyLevel' => 'Beginner to Intermediate',
    );

    echo '<script type="application/ld+json">' . wp_json_encode( $schema, JSON_UNESCAPED_SLASHES | JSON_PRETTY_PRINT ) . '</script>' . "\n";
}
add_action( 'wp_head', 'codesphere_output_schema', 20 );

/**
 * Safely resolve the permalink for an article by its slug.
 *
 * Uses get_page_by_path() and get_permalink() to resolve the true WordPress permalink.
 *
 * @param string $slug Post or page slug.
 * @param string $fallback_path Optional path to use if post is not found.
 * @return string The resolved permalink or fallback URL.
 */
function codesphere_get_post_permalink( $slug, $fallback_path = '' ) {
    $clean_slug = trim( $slug, '/' );
    $leaf_slug  = basename( $clean_slug );

    // 1. Try resolving by leaf slug or path as post
    $post = get_page_by_path( $leaf_slug, OBJECT, 'post' );
    if ( ! $post && $leaf_slug !== $clean_slug ) {
        $post = get_page_by_path( $clean_slug, OBJECT, 'post' );
    }

    // 2. Try resolving as page
    if ( ! $post ) {
        $post = get_page_by_path( $leaf_slug, OBJECT, 'page' );
        if ( ! $post && $leaf_slug !== $clean_slug ) {
            $post = get_page_by_path( $clean_slug, OBJECT, 'page' );
        }
    }

    // 3. Fallback check with post_type array
    if ( ! $post ) {
        $post = get_page_by_path( $leaf_slug, OBJECT, array( 'post', 'page' ) );
    }

    if ( $post && ! is_wp_error( $post ) ) {
        $permalink = get_permalink( $post );
        if ( ! empty( $permalink ) && ! is_wp_error( $permalink ) ) {
            return $permalink;
        }
    }

    if ( ! empty( $fallback_path ) ) {
        return home_url( $fallback_path );
    }

    return home_url( '/' . $clean_slug . '/' );
}

/**
 * Safely resolve a cluster / category archive or page URL.
 *
 * @param string $slug Category or page slug.
 * @return string The resolved URL.
 */
function codesphere_get_cluster_url( $slug ) {
    $clean_slug = trim( $slug, '/' );

    // 1. Check if a page exists with this slug
    $page = get_page_by_path( $clean_slug, OBJECT, array( 'page', 'post' ) );
    if ( $page && ! is_wp_error( $page ) ) {
        $permalink = get_permalink( $page );
        if ( ! empty( $permalink ) && ! is_wp_error( $permalink ) ) {
            return $permalink;
        }
    }

    // 2. Check if a category exists with this slug
    $category = get_category_by_slug( $clean_slug );
    if ( $category && ! is_wp_error( $category ) ) {
        $cat_link = get_category_link( $category->term_id );
        if ( $cat_link && ! is_wp_error( $cat_link ) ) {
            return $cat_link;
        }
    }

    return home_url( '/' . $clean_slug . '/' );
}

/**
 * Safely resolve the "Roadmaps & Guides" navigation URL.
 *
 * Checks for a page first, then category archive, then fallback without hardcoding /blog/.
 *
 * @return string Working URL.
 */
function codesphere_get_roadmaps_url() {
    // 1. Check if a page exists for blog or roadmaps
    foreach ( array( 'blog', 'roadmaps-guides', 'roadmaps' ) as $slug ) {
        $page = get_page_by_path( $slug, OBJECT, array( 'page', 'post' ) );
        if ( $page && ! is_wp_error( $page ) ) {
            $permalink = get_permalink( $page );
            if ( ! empty( $permalink ) && ! is_wp_error( $permalink ) ) {
                return $permalink;
            }
        }
    }

    // 2. Check if a category exists (XML imports category with nicename 'blog')
    foreach ( array( 'blog', 'roadmaps-guides', 'roadmaps' ) as $cat_slug ) {
        $cat = get_category_by_slug( $cat_slug );
        if ( $cat && ! is_wp_error( $cat ) ) {
            $link = get_category_link( $cat->term_id );
            if ( $link && ! is_wp_error( $link ) ) {
                return $link;
            }
        }
    }

    // 3. Fallback to posts page or home
    $posts_page_id = get_option( 'page_for_posts' );
    if ( $posts_page_id ) {
        return get_permalink( $posts_page_id );
    }

    return home_url( '/' );
}

/**
 * Filter post content to resolve legacy pseudo-hierarchical internal links to canonical permalinks.
 *
 * Rewrites internal links such as /dsa/trees/binary-trees/, /programming/variables-data-types/,
 * /blog/binary-tree-vs-binary-search-tree/ in imported post content to the active Post Name permalinks.
 *
 * @param string $content Post content.
 * @return string Filtered content with valid permalinks.
 */
function codesphere_filter_content_internal_links( $content ) {
    if ( empty( $content ) ) {
        return $content;
    }

    return preg_replace_callback(
        '/<a\s+([^>]*?)href=(["\'])(.*?)\2([^>]*)>/i',
        function ( $matches ) {
            $prefix = $matches[1];
            $quote  = $matches[2];
            $href   = trim( $matches[3] );
            $suffix = $matches[4];

            $home_url = home_url();
            $path = '';

            if ( strpos( $href, $home_url ) === 0 ) {
                $path = substr( $href, strlen( $home_url ) );
            } elseif ( strpos( $href, 'http://' ) !== 0 && strpos( $href, 'https://' ) !== 0 && strpos( $href, '//' ) !== 0 && strpos( $href, '#' ) !== 0 && strpos( $href, 'mailto:' ) !== 0 ) {
                $path = $href;
            }

            if ( ! empty( $path ) ) {
                $trimmed = trim( $path, '/' );
                $parts = explode( '/', $trimmed );
                $clusters = array( 'programming', 'dsa', 'web-development', 'computer-science', 'blog' );

                if ( ! empty( $parts ) && in_array( $parts[0], $clusters, true ) ) {
                    $leaf_slug = end( $parts );
                    if ( ! empty( $leaf_slug ) ) {
                        $resolved = codesphere_get_post_permalink( $leaf_slug );
                        if ( $resolved ) {
                            return '<a ' . $prefix . 'href=' . $quote . esc_url( $resolved ) . $quote . $suffix . '>';
                        }
                    }
                }
            }

            return $matches[0];
        },
        $content
    );
}
add_filter( 'the_content', 'codesphere_filter_content_internal_links', 20 );

/**
 * Handle virtual /robots.txt request within WordPress subdirectory installation.
 */
function codesphere_handle_virtual_robots() {
    if ( isset( $_SERVER['REQUEST_URI'] ) && preg_match( '#/robots\.txt/?(\?.*)?$#i', $_SERVER['REQUEST_URI'] ) ) {
        header( 'Content-Type: text/plain; charset=utf-8' );
        header( 'X-Robots-Tag: noindex, follow' );
        echo "User-agent: *\n";
        echo "Disallow: /wp-admin/\n";
        echo "Allow: /wp-admin/admin-ajax.php\n";
        echo "\nSitemap: " . esc_url( home_url( '/sitemap.xml' ) ) . "\n";
        exit;
    }
}
add_action( 'init', 'codesphere_handle_virtual_robots', 1 );


