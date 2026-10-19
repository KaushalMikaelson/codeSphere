<?php
/**
 * Schema.org Structured Data Generator for Educational Courses & Topics
 *
 * @package CodeSphere_Learning_Links
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

class CodeSphere_Learning_Links_Schema {

    public static function init() {
        add_action( 'wp_head', array( __CLASS__, 'output_educational_schema' ), 25 );
    }

    public static function output_educational_schema() {
        if ( ! is_singular( array( 'post', 'page' ) ) ) {
            return;
        }

        $post_id = get_the_ID();
        $links_data = get_post_meta( $post_id, '_codesphere_learning_links', true );

        if ( empty( $links_data ) || ! is_array( $links_data ) ) {
            return;
        }

        $schema = array(
            '@context'         => 'https://schema.org',
            '@type'            => 'LearningResource',
            'name'             => get_the_title(),
            'description'      => wp_strip_all_tags( get_the_excerpt() ),
            'url'              => get_permalink(),
            'learningResourceType' => 'Concept Guide',
            'educationalLevel' => 'Undergraduate Computer Science',
            'teaches'          => get_the_title(),
        );

        // Competency prerequisites
        if ( ! empty( $links_data['prerequisites'] ) ) {
            $prereqs = array();
            foreach ( $links_data['prerequisites'] as $item ) {
                if ( ! empty( $item['title'] ) ) {
                    $prereqs[] = $item['title'];
                }
            }
            if ( ! empty( $prereqs ) ) {
                $schema['competencyRequired'] = implode( ', ', $prereqs );
            }
        }

        echo '<script type="application/ld+json">' . wp_json_encode( $schema, JSON_UNESCAPED_SLASHES | JSON_PRETTY_PRINT ) . '</script>' . "\n";
    }
}
