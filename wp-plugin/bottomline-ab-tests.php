<?php
/*
Plugin Name: BottomLine AB Tests
Description: Simple A/B testing plugin for CTA text.
Version: 0.1.0
*/

if (!defined('ABSPATH')) exit;

function bl_ab_default_options() {
    add_option('bl_ab_tracking_enabled', 1);
    add_option('bl_ab_notice_dismissed', 0);
}
register_activation_hook(__FILE__, 'bl_ab_default_options');

function bl_ab_admin_notice(){
    if(!current_user_can('manage_options')) return;
    $dismissed = get_option('bl_ab_notice_dismissed', 0);
    if(!$dismissed){
        echo '<div class="notice notice-info is-dismissible"><p>'; 
        echo 'We run anonymous A/B tests and track clicks. No personal data is collected. You can opt out any time in plugin settings.';
        echo '</p></div>';
        update_option('bl_ab_notice_dismissed', 1);
    }
}
add_action('admin_notices','bl_ab_admin_notice');

function bl_ab_settings_menu(){
    add_options_page('BottomLine AB Tests','BottomLine AB Tests','manage_options','bl-ab-tests','bl_ab_settings_page');
}
add_action('admin_menu','bl_ab_settings_menu');

function bl_ab_settings_page(){
    if(isset($_POST['bl_ab_save'])){
        update_option('bl_ab_tracking_enabled', isset($_POST['bl_ab_tracking_enabled']) ? 1 : 0);
        echo '<div class="updated"><p>Settings saved.</p></div>';
    }
    $checked = get_option('bl_ab_tracking_enabled',1) ? 'checked' : '';
    echo '<div class="wrap"><h1>BottomLine AB Tests</h1>'; 
    echo '<form method="post"><label><input type="checkbox" name="bl_ab_tracking_enabled" '.$checked.'> Enable tracking</label><br><br>'; 
    echo '<input type="submit" name="bl_ab_save" class="button button-primary" value="Save" />';
    echo '</form></div>';
}

function bl_ab_enqueue_scripts(){
    $tracking = get_option('bl_ab_tracking_enabled',1);
    wp_enqueue_script('bl-ab-client',plugins_url('dist/ab-client.min.js', __FILE__),[],null,true);
    wp_localize_script('bl-ab-client','blAbConfig',['trackingEnabled'=>boolval($tracking)]);
}
add_action('wp_enqueue_scripts','bl_ab_enqueue_scripts');

function bl_ab_create_sample_page(){
    if(get_option('bl_ab_sample_page_created')) return;
    $content = '<button id="cta-test-btn" data-ab-id="cta-test-btn">Join Now</button>';
    $page_id = wp_insert_post([
        'post_title' => 'A/B Test Sample Page',
        'post_content' => $content,
        'post_status' => 'publish',
        'post_type' => 'page'
    ]);
    if($page_id) update_option('bl_ab_sample_page_created',$page_id);
}
register_activation_hook(__FILE__,'bl_ab_create_sample_page');
?>
