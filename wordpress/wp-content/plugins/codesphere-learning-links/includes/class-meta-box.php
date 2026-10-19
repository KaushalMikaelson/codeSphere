<?php
/**
 * Meta Box Manager for Learning Links
 *
 * @package CodeSphere_Learning_Links
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

class CodeSphere_Learning_Links_Meta_Box {

    public static function init() {
        add_action( 'add_meta_boxes', array( __CLASS__, 'add_meta_box' ) );
        add_action( 'save_post', array( __CLASS__, 'save_meta_box' ) );
    }

    public static function add_meta_box() {
        add_meta_box(
            'codesphere_learning_links_box',
            __( 'CodeSphere Learning Pathways & Internal Links', 'codesphere-learning-links' ),
            array( __CLASS__, 'render_box' ),
            array( 'post', 'page' ),
            'normal',
            'high'
        );
    }

    public static function render_box( $post ) {
        wp_nonce_field( 'codesphere_learning_links_save', 'codesphere_learning_links_nonce' );
        $links_data = get_post_meta( $post->ID, '_codesphere_learning_links', true );

        if ( ! is_array( $links_data ) ) {
            $links_data = array(
                'parent_hub'     => array( array( 'title' => '', 'url' => '', 'description' => '' ) ),
                'prerequisites'  => array( array( 'title' => '', 'url' => '', 'description' => '' ) ),
                'next_topics'    => array( array( 'title' => '', 'url' => '', 'description' => '' ) ),
                'related_topics' => array( array( 'title' => '', 'url' => '', 'description' => '' ) ),
            );
        }

        $sections = array(
            'parent_hub'     => __( 'Parent Topic Hub (e.g. /dsa/trees/)', 'codesphere-learning-links' ),
            'prerequisites'  => __( 'Prerequisites (e.g. Recursion for Binary Trees)', 'codesphere-learning-links' ),
            'next_topics'    => __( 'Next Topics (e.g. Tree Traversal, BST)', 'codesphere-learning-links' ),
            'related_topics' => __( 'Related Topics (e.g. Dynamic Programming)', 'codesphere-learning-links' ),
        );

        echo '<div class="codesphere-meta-box-wrap" style="padding: 10px 0;">';
        echo '<p style="color: #64748b; font-size: 13px;">' . esc_html__( 'Configure contextual internal links to build crawlable curriculum graphs and eliminate orphan pages.', 'codesphere-learning-links' ) . '</p>';

        foreach ( $sections as $key => $label ) {
            $items = ! empty( $links_data[ $key ] ) ? $links_data[ $key ] : array( array( 'title' => '', 'url' => '', 'description' => '' ) );
            echo '<div style="margin-bottom: 20px; background: #f8fafc; padding: 15px; border: 1px solid #e2e8f0; border-radius: 6px;">';
            echo '<h4 style="margin: 0 0 10px 0; color: #1e293b;">' . esc_html( $label ) . '</h4>';

            foreach ( $items as $i => $item ) {
                $title = isset( $item['title'] ) ? $item['title'] : '';
                $url   = isset( $item['url'] ) ? $item['url'] : '';
                $desc  = isset( $item['description'] ) ? $item['description'] : '';

                echo '<div style="display: flex; gap: 10px; margin-bottom: 8px;">';
                echo '<input type="text" name="codesphere_links[' . esc_attr( $key ) . '][' . $i . '][title]" value="' . esc_attr( $title ) . '" placeholder="Anchor Text (e.g., Recursion Explained)" style="flex: 1;" />';
                echo '<input type="text" name="codesphere_links[' . esc_attr( $key ) . '][' . $i . '][url]" value="' . esc_attr( $url ) . '" placeholder="Relative or Absolute URL (/dsa/algorithms/recursion/)" style="flex: 1;" />';
                echo '<input type="text" name="codesphere_links[' . esc_attr( $key ) . '][' . $i . '][description]" value="' . esc_attr( $desc ) . '" placeholder="Contextual note / summary" style="flex: 1.5;" />';
                echo '</div>';
            }

            echo '</div>';
        }

        echo '</div>';
    }

    public static function save_meta_box( $post_id ) {
        if ( ! isset( $_POST['codesphere_learning_links_nonce'] ) ) {
            return;
        }
        if ( ! wp_verify_nonce( $_POST['codesphere_learning_links_nonce'], 'codesphere_learning_links_save' ) ) {
            return;
        }
        if ( defined( 'DOING_AUTOSAVE' ) && DOING_AUTOSAVE ) {
            return;
        }
        if ( ! current_user_can( 'edit_post', $post_id ) ) {
            return;
        }

        if ( isset( $_POST['codesphere_links'] ) && is_array( $_POST['codesphere_links'] ) ) {
            $clean_data = array();
            foreach ( $_POST['codesphere_links'] as $section => $rows ) {
                $clean_data[ $section ] = array();
                foreach ( $rows as $row ) {
                    $title = sanitize_text_field( $row['title'] ?? '' );
                    $url   = esc_url_raw( $row['url'] ?? '' );
                    $desc  = sanitize_text_field( $row['description'] ?? '' );

                    if ( ! empty( $title ) && ! empty( $url ) ) {
                        $clean_data[ $section ][] = array(
                            'title'       => $title,
                            'url'         => $url,
                            'description' => $desc,
                        );
                    }
                }
            }
            update_post_meta( $post_id, '_codesphere_learning_links', $clean_data );
        }
    }
}
