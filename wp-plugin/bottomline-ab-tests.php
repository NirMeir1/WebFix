<?php
/*
Plugin Name: BottomLine AB Tests
Description: Injects JS for anonymous A/B testing.
*/

if (!defined('ABSPATH')) exit;

const BL_AB_OPTION = 'bottomline_ab_enabled';

// Activation: set default option
register_activation_hook(__FILE__, function() {
    if (get_option(BL_AB_OPTION) === false) {
        add_option(BL_AB_OPTION, '1');
    }
});

// Deactivation: remove option
register_deactivation_hook(__FILE__, function() {
    delete_option(BL_AB_OPTION);
});

add_action('admin_notices', function() {
    if (!current_user_can('manage_options')) return;
    echo '<div class="notice notice-info is-dismissible"><p>We run anonymous A/B tests and track clicks. No personal data is collected. You can opt out any time in plugin settings.</p></div>';
});

function bl_ab_register_settings() {
    register_setting('bl_ab_options', BL_AB_OPTION);
}
add_action('admin_init', 'bl_ab_register_settings');

function bl_ab_options_page() {
    ?>
    <div class="wrap">
        <h1>BottomLine A/B Tests</h1>
        <form method="post" action="options.php">
            <?php settings_fields('bl_ab_options'); ?>
            <table class="form-table" role="presentation">
                <tr valign="top">
                    <th scope="row">Enable Tracking</th>
                    <td><input type="checkbox" name="<?php echo BL_AB_OPTION; ?>" value="1" <?php checked('1', get_option(BL_AB_OPTION, '1')); ?> /></td>
                </tr>
            </table>
            <?php submit_button(); ?>
        </form>
    </div>
    <?php
}

function bl_ab_add_options_page() {
    add_options_page('BottomLine AB Tests', 'BottomLine AB Tests', 'manage_options', 'bl-ab-tests', 'bl_ab_options_page');
}
add_action('admin_menu', 'bl_ab_add_options_page');

function bl_ab_enqueue_script() {
    if (get_option(BL_AB_OPTION, '1') !== '1') return;
    $script = plugin_dir_url(__FILE__) . 'dist/ab-client.min.js';
    wp_enqueue_script('bl-ab-client', $script, array(), null, true);
    $enabled = get_option(BL_AB_OPTION, '1') === '1' ? 'true' : 'false';
    wp_localize_script('bl-ab-client', 'BL_AB_CONFIG', array('enabled' => $enabled));
}
add_action('wp_enqueue_scripts', 'bl_ab_enqueue_script');
?>
