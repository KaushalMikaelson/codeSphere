<?php
/**
 * Header Template for CodeSphere
 *
 * @package CodeSphere
 */
?><!DOCTYPE html>
<html <?php language_attributes(); ?>>
<head>
    <meta charset="<?php bloginfo( 'charset' ); ?>">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="profile" href="https://gmpg.org/xfn/11">
    <?php wp_head(); ?>
</head>
<body <?php body_class(); ?>>
<?php wp_body_open(); ?>

<a class="skip-link" href="#primary-content"><?php esc_html_e( 'Skip to primary content', 'codesphere' ); ?></a>

<header class="site-header" role="banner">
    <div class="site-container header-inner">
        <a href="<?php echo esc_url( home_url( '/' ) ); ?>" class="site-branding" rel="home">
            <div class="site-logo-icon" aria-hidden="true">&lt;/&gt;</div>
            <div>
                <span class="site-title"><?php bloginfo( 'name' ); ?></span>
                <span class="site-tagline"><?php bloginfo( 'description' ); ?></span>
            </div>
        </a>

        <nav class="main-navigation" role="navigation" aria-label="<?php esc_attr_e( 'Main Clusters Navigation', 'codesphere' ); ?>">
            <?php
            if ( has_nav_menu( 'primary' ) ) {
                wp_nav_menu( array(
                    'theme_location' => 'primary',
                    'container'      => false,
                    'fallback_cb'    => false,
                ) );
            } else {
                // Semantic fallback navigation representing the 4 core topic clusters
                ?>
                <ul>
                    <li><a href="<?php echo esc_url( codesphere_get_cluster_url( 'programming' ) ); ?>" class="nav-cluster-prog"><?php esc_html_e( 'Programming', 'codesphere' ); ?></a></li>
                    <li><a href="<?php echo esc_url( codesphere_get_cluster_url( 'dsa' ) ); ?>" class="nav-cluster-dsa"><?php esc_html_e( 'DSA', 'codesphere' ); ?></a></li>
                    <li><a href="<?php echo esc_url( codesphere_get_cluster_url( 'web-development' ) ); ?>" class="nav-cluster-web"><?php esc_html_e( 'Web Dev', 'codesphere' ); ?></a></li>
                    <li><a href="<?php echo esc_url( codesphere_get_cluster_url( 'computer-science' ) ); ?>" class="nav-cluster-cs"><?php esc_html_e( 'Core CS', 'codesphere' ); ?></a></li>
                    <li><a href="<?php echo esc_url( codesphere_get_roadmaps_url() ); ?>"><?php esc_html_e( 'Roadmaps & Guides', 'codesphere' ); ?></a></li>
                </ul>
                <?php
            }
            ?>
        </nav>
    </div>
</header>

<div class="site-container">
    <?php codesphere_breadcrumbs(); ?>
</div>

<main id="primary-content" class="site-content" role="main">
    <div class="site-container">
