module.exports = function(grunt) {
    grunt.initConfig({
        less: {
            development: {
                files: {
                    "pythoncad_qt/stylesheets/pythoncad_qt.css": "pythoncad_qt/stylesheets/pythoncad_qt.less"
                }
            }
        },
        watch: {
            styles: {
                files: ['pythoncad_qt/stylesheets/*.less'],
                tasks: ['less']
            }
        }
    });
    grunt.loadNpmTasks('grunt-contrib-less');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.registerTask('default', ['watch']);
};
