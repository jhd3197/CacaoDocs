// craco.config.js
const HtmlWebpackPlugin = require('html-webpack-plugin');
const HtmlInlineScriptPlugin = require('html-inline-script-webpack-plugin');
const path = require('path');

module.exports = {
    webpack: {
        configure: (webpackConfig) => {
            // Ignore source map warnings
            webpackConfig.ignoreWarnings = [/Failed to parse source map/];
            
            // Modify output configuration
            webpackConfig.output = {
                ...webpackConfig.output,
                filename: 'bundle.js',
                assetModuleFilename: 'images/[hash][ext][query]', // Optional: Customize asset filenames
            };

            // Remove existing HtmlWebpackPlugin instances
            webpackConfig.plugins = webpackConfig.plugins.filter(
                plugin => !(plugin instanceof HtmlWebpackPlugin)
            );

            // Add new HtmlWebpackPlugin with html-loader
            webpackConfig.plugins.push(
                new HtmlWebpackPlugin({
                    template: path.resolve(__dirname, 'public/index.html'),
                    inject: 'body',
                    minify: {
                        removeComments: true,
                        collapseWhitespace: true,
                        removeRedundantAttributes: true,
                        useShortDoctype: true,
                        removeEmptyAttributes: true,
                        removeStyleLinkTypeAttributes: true,
                        keepClosingSlash: true,
                        minifyJS: true,
                        minifyCSS: true,
                        minifyURLs: true,
                    },
                    // Use html-loader to process the template
                    templateParameters: {}, // Can be customized as needed
                }),
                new HtmlInlineScriptPlugin({
                    scriptMatchPattern: [/bundle\.js$/],
                    htmlMatchPattern: [/index\.html$/],
                })
            );

            // Inline CSS
            webpackConfig.optimization = {
                ...webpackConfig.optimization,
                splitChunks: {
                    cacheGroups: {
                        styles: {
                            name: 'styles',
                            type: 'css/mini-extract',
                            chunks: 'all',
                            enforce: true,
                        },
                    },
                },
            };

            // Add html-loader to handle images in HTML templates
            const htmlRule = {
                test: /\.html$/,
                use: [
                    {
                        loader: 'html-loader',
                        options: {
                            sources: {
                                list: [
                                    // All default supported tags and attributes
                                    '...',
                                    {
                                        tag: 'img',
                                        attribute: 'src',
                                        type: 'src',
                                    },
                                    // Add more if you have other tags that include images
                                ],
                            },
                            minimize: false, // Let HtmlWebpackPlugin handle minification
                        },
                    },
                ],
            };

            // Insert html-loader before HtmlWebpackPlugin
            webpackConfig.module.rules.unshift(htmlRule);

            // Configure asset modules for images to inline them as Base64
            const assetRule = {
                test: /\.(png|jpe?g|gif|svg)$/i,
                type: 'asset/inline',
            };

            // Ensure asset rule is included
            webpackConfig.module.rules.push(assetRule);

            return webpackConfig;
        },
    },
};
