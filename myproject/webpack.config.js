const path = require('path');
const BundleTracker = require('webpack-bundle-tracker');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const CssMinimizerPlugin = require('css-minimizer-webpack-plugin');

// One config for both modes:
//   npm run watch  -> webpack --mode development --watch
//   npm run build  -> webpack --mode production
module.exports = (env, argv) => {
    const isProd = argv.mode === 'production';

    return {
        context: __dirname,
        mode: isProd ? 'production' : 'development',

        // Entry point. Templates load it with {% render_bundle 'main' %}
        entry: {
            main: './static/js/script.js',
        },

        output: {
            path: path.resolve(__dirname, 'static/bundles'),
            publicPath: '/static/bundles/',
            filename: '[name]-[contenthash].js',
            assetModuleFilename: 'assets/[name]-[contenthash][ext]',
            clean: true,
        },

        devtool: isProd ? false : 'source-map',

        plugins: [
            // Writes webpack-stats.json, read by django-webpack-loader
            new BundleTracker({ path: __dirname, filename: 'webpack-stats.json' }),
            new MiniCssExtractPlugin({ filename: '[name]-[contenthash].css' }),
        ],

        module: {
            rules: [
                {
                    test: /\.m?js$/,
                    exclude: /node_modules/,
                    use: 'babel-loader', // see babel.config.json
                },
                {
                    test: /\.s?css$/i,
                    use: [
                        MiniCssExtractPlugin.loader,
                        { loader: 'css-loader', options: { sourceMap: !isProd } },
                        { loader: 'postcss-loader', options: { sourceMap: !isProd } }, // see postcss.config.js
                        { loader: 'sass-loader', options: { sourceMap: !isProd } },
                    ],
                },
                {
                    // Images referenced from CSS/JS: inlined if small, emitted otherwise
                    test: /\.(png|jpe?g|gif|svg|webp|avif)$/i,
                    type: 'asset',
                },
                {
                    test: /\.(woff2?|ttf|otf)$/i,
                    type: 'asset/resource',
                },
            ],
        },

        optimization: {
            minimizer: [
                '...', // keep the default JS minimizer (terser)
                new CssMinimizerPlugin(),
            ],
        },

        performance: {
            hints: isProd ? 'warning' : false,
            // Fonts are loaded on demand by the browser; don't warn about them
            assetFilter: (file) => !/\.(woff2?|ttf|otf|map)$/.test(file),
        },
    };
};
