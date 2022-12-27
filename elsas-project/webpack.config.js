var path = require("path");
var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const CssMinimizerPlugin = require("css-minimizer-webpack-plugin");

module.exports = {
    context: __dirname,
    devtool: 'source-map',
    entry: './static/js/script', // entry point of our app. assets/js/index.js should require other js modules and dependencies it needs

    output: {
        path: path.resolve('./static/bundles/'),
        publicPath: '/static/bundles/',
        filename: "[name]-[fullhash].js",
        clean: true,
    },
    watch: true,
    mode: 'development',

    plugins: [
        new BundleTracker({filename: './webpack-stats.json'}),
        new MiniCssExtractPlugin({
                filename: 'styles.[contenthash].css'
        }),
        // new OptimizeCssAssetsPlugin({ // cambiado por el CssMinimizerPlugin recomendado para webpack5+
        //     cssProcessor: require('cssnano'),
        //     cssProcessorOptions: {
        //         map: {
        //             inline: false,
        //         },
        //         discardComments: {
        //             removeAll: true
        //         },
        //         discardUnused: false
        //     },
        //     canPrint: true
        // }),
        new webpack.ProvidePlugin({
            $: "jquery",
            jQuery: "jquery"
        }),
    ],

    module: {
        rules: [

            { // to transform JSX into JS
                test: /\.jsx?$/, 
                exclude: /node_modules/, 
                loader: 'babel-loader'
            },    

            //   // typescript
            // needs ts-loader and typescript dependencies
            // also configuring tsconfig.jsn
            //   {
            //     test: /\.ts?$/,
            //     use: 'ts-loader',
            //     exclude: /node_modules/,
            //   },

            {
                test: /\.s?css$/i,
                use: [

                    MiniCssExtractPlugin.loader, 

                    // {
                    //     // creates style nodes from JS strings
                    //     loader: "style-loader",
                    //     options: {
                    //         //sourceMap: true // se tiene que poner en el loader anterior (en nuestro caso css-loader)
                    //         // injectType: 'singletonStyleTag'
                    //     }
                    // },

                    {
                        // translates CSS into CommonJS
                        loader: "css-loader",
                        options: {
                            sourceMap: true
                        }
                    },

                    // Please note we are not running postcss in development mode
                    // post-css
                    // {
                    //     loader: "postcss-loader",
                    //     options: {
                    //       postcssOptions: {
                    //         plugins: [
                    //           [
                    //             "postcss-preset-env",
                    //             "autoprefixer",
                    //             {
                    //               // Options
                    //             },
                    //           ],
                    //         ],
                    //       },
                    //     },
                    // },

                    {
                        // compiles Sass to CSS
                        loader: "sass-loader",
                        options: {
                            // outputStyle: 'expanded', // nueva forma de poner opción abajo
                            sassOptions: {
                                outputStyle: "expanded",
                            },
                            sourceMap: true,
                            // sourceMapContents: true // no es necesaria, se ponepor defecto con sourceMap true
                        }
                    },
                    // {
                    //     // Load all images as base64 encoding if they are smaller than 8192 bytes
                    //     test: /\.(png|jpg|gif)$/,
                    //     use: [
                    //         {
                    //             loader: 'url-loader',
                    //             options: {
                    //                 // On development we want to see where the file is coming from, hence we preserve the [path]
                    //                 name: '[path][name].[ext]?hash=[hash:20]',
                    //                 limit: 8192
                    //             }
                    //         }
                    //     ]
                    // }
                    // ,
                    // {
                    //     // Load all icons
                    //     test: /\.(eot|woff|woff2|svg|ttf)([\?]?.*)$/,
                    //     use: [
                    //         {
                    //             loader: 'file-loader',
                    //         }
                    //     ]
                    // },
                ],
            },
        ],
    },

    resolve: {
        modules: ['node_modules'],
        extensions: ['', '.js']
    },

    optimization: {
        minimizer: [
            `...`, // webpack@5 feature: extend existing minimizers (i.e. `terser-webpack-plugin`)
            new CssMinimizerPlugin(),
        ],
    },
}
