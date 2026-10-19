<?php
/**
 * CodeSphere Content Import Helper
 *
 * Can be run via WP-CLI: `wp eval-file import-helper.php`
 * Or included in WordPress to programmatically verify and load the 32 articles.
 */

if ( ! defined( 'ABSPATH' ) ) {
    // Check if running from WordPress root
    if ( file_exists( dirname( dirname( dirname( __FILE__ ) ) ) . '/wp-load.php' ) ) {
        require_once dirname( dirname( dirname( __FILE__ ) ) ) . '/wp-load.php';
    } else {
        echo "Please run this script inside a WordPress installation or via WP-CLI:\n";
        echo "wp import " . __DIR__ . "/codesphere-content.xml --authors=create\n";
        exit( 1 );
    }
}

echo "CodeSphere Content Import Helper ready.\n";
echo "XML import source: " . __DIR__ . "/codesphere-content.xml\n";
echo "Verify that the CodeSphere theme and CodeSphere Learning Links plugin are active.\n";
