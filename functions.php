<?php
if ( ! defined( 'ABSPATH' ) ) { exit; }
function ondex_fulfilment_setup() {
    add_theme_support( 'title-tag' );
    add_theme_support( 'post-thumbnails' );
    add_theme_support( 'html5', array('search-form','comment-form','comment-list','gallery','caption','style','script') );
    add_theme_support( 'responsive-embeds' );
    add_theme_support( 'automatic-feed-links' );
}
add_action( 'after_setup_theme', 'ondex_fulfilment_setup' );
function ondex_fulfilment_assets() {
    wp_enqueue_style(
        'ondex-fonts',
        'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Space+Mono:wght@400;700&display=swap',
        array(),
        null
    );
    wp_enqueue_style( 'ondex-theme', get_stylesheet_uri(), array( 'ondex-fonts' ), wp_get_theme()->get('Version') );
}
add_action( 'wp_enqueue_scripts', 'ondex_fulfilment_assets' );

function ondex_fulfilment_resource_hints( $urls, $relation_type ) {
    if ( 'preconnect' === $relation_type ) {
        $urls[] = 'https://fonts.googleapis.com';
        $urls[] = array(
            'href'        => 'https://fonts.gstatic.com',
            'crossorigin' => 'anonymous',
        );
    }

    return $urls;
}
add_filter( 'wp_resource_hints', 'ondex_fulfilment_resource_hints', 10, 2 );

/**
 * Use the built-in SEO output only when no dedicated SEO plugin is active.
 */
function ondex_fulfilment_has_seo_plugin() {
    return defined( 'WPSEO_VERSION' )
        || defined( 'RANK_MATH_VERSION' )
        || defined( 'AIOSEO_VERSION' )
        || class_exists( 'AIOSEO\\Plugin\\AIOSEO' );
}

function ondex_fulfilment_front_title( $title ) {
    if ( ! ondex_fulfilment_has_seo_plugin() && is_front_page() ) {
        return 'E-commerce fulfilment voor webshops & marketplaces | Ondex';
    }

    return $title;
}
add_filter( 'pre_get_document_title', 'ondex_fulfilment_front_title', 20 );

function ondex_fulfilment_meta_description() {
    if ( is_front_page() ) {
        return 'Ondex Fulfilment verzorgt opslag, orderverwerking, verzending en retouren voor webshops en marketplaces, met realtime WMS-inzicht en één all-in tarief.';
    }

    if ( is_singular() && has_excerpt() ) {
        return wp_strip_all_tags( get_the_excerpt() );
    }

    return wp_strip_all_tags( get_bloginfo( 'description' ) );
}

function ondex_fulfilment_seo_meta() {
    if ( ondex_fulfilment_has_seo_plugin() ) {
        return;
    }

    $description = ondex_fulfilment_meta_description();
    $request     = isset( $GLOBALS['wp']->request ) ? $GLOBALS['wp']->request : '';
    $canonical   = is_front_page() ? home_url( '/' ) : ( is_singular() ? get_permalink() : home_url( '/' . ltrim( $request, '/' ) ) );
    $title       = wp_get_document_title();
    $image       = get_template_directory_uri() . '/assets/images/asset-eacebf2d3db0.webp';

    if ( $description ) {
        printf( "\n<meta name=\"description\" content=\"%s\">", esc_attr( $description ) );
    }
    printf( "\n<link rel=\"canonical\" href=\"%s\">", esc_url( $canonical ) );
    printf( "\n<meta property=\"og:locale\" content=\"nl_NL\">" );
    printf( "\n<meta property=\"og:type\" content=\"website\">" );
    printf( "\n<meta property=\"og:site_name\" content=\"Ondex Fulfilment\">" );
    printf( "\n<meta property=\"og:title\" content=\"%s\">", esc_attr( $title ) );
    printf( "\n<meta property=\"og:description\" content=\"%s\">", esc_attr( $description ) );
    printf( "\n<meta property=\"og:url\" content=\"%s\">", esc_url( $canonical ) );
    printf( "\n<meta property=\"og:image\" content=\"%s\">", esc_url( $image ) );
    printf( "\n<meta property=\"og:image:width\" content=\"1616\">" );
    printf( "\n<meta property=\"og:image:height\" content=\"1050\">" );
    printf( "\n<meta property=\"og:image:alt\" content=\"Ondex Fulfilment magazijn en orderverwerking\">" );
    printf( "\n<meta name=\"twitter:card\" content=\"summary_large_image\">" );
    printf( "\n<meta name=\"twitter:title\" content=\"%s\">", esc_attr( $title ) );
    printf( "\n<meta name=\"twitter:description\" content=\"%s\">", esc_attr( $description ) );
    printf( "\n<meta name=\"twitter:image\" content=\"%s\">\n", esc_url( $image ) );

    if ( is_front_page() ) {
        $schema = array(
            '@context'     => 'https://schema.org',
            '@type'        => 'Organization',
            '@id'          => home_url( '/#organization' ),
            'name'         => 'Ondex Fulfilment',
            'url'          => home_url( '/' ),
            'logo'         => get_template_directory_uri() . '/assets/svg/asset-b9aac6265fae.svg',
            'description'  => $description,
            'email'        => 'info@ondexfulfilment.nl',
            'telephone'    => '+31 85 060 2274',
            'address'      => array(
                '@type'           => 'PostalAddress',
                'streetAddress'   => 'Aalsbergen 10',
                'postalCode'      => '6942 SE',
                'addressLocality' => 'Didam',
                'addressCountry'  => 'NL',
            ),
            'sameAs'       => array(
                'https://www.linkedin.com/company/ondexfulfilment',
                'https://www.instagram.com/ondexfulfilment.nl/',
                'https://www.tiktok.com/@ondexfulfilment.nl',
            ),
            'contactPoint' => array(
                '@type'       => 'ContactPoint',
                'telephone'   => '+31 85 060 2274',
                'contactType' => 'customer service',
                'availableLanguage' => array( 'nl', 'en' ),
            ),
        );

        printf(
            "\n<script type=\"application/ld+json\">%s</script>\n",
            wp_json_encode( $schema, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE )
        );
    }
}
add_action( 'wp_head', 'ondex_fulfilment_seo_meta', 2 );
