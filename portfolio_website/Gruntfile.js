module.exports = function(grunt) {
  grunt.initConfig({
    responsive_images: {
      dev: {
        options: {
          engine: 'im',
          sizes: [{
            name: "small",
            width: "480",
            suffix: "",
            quality: 50,
          },
          {
            name: "medium",
            width: "720",
            suffix: "",
            quality: 50,
          },
          {
            name: "large",
            width: "1080",
            suffix: "",
            quality: 50,
          }]
        },

        files: [{
          expand: true,
          src: ['*.{gif,jpg,jpeg,png}'],
          cwd: 'img/',
          dest: 'img_rsp/'
        }]
      }
    },

    /* Clear out the images directory if it exists */
    clean: {
      dev: {
        src: ['img_rsp'],
      },
    },

    /* Generate the images directory if it is missing */
    mkdir: {
      dev: {
        options: {
          create: ['img_rsp']
        },
      },
    },

    copy: {
      dev: {
        files: [{
          expand: true,
          src: 'img/fixed/*.{gif,jpg,png}',
          dest: 'img_rsp/'
        }]
      },
    },

  });

  grunt.loadNpmTasks('grunt-responsive-images');
  grunt.loadNpmTasks('grunt-contrib-clean');
  grunt.loadNpmTasks('grunt-contrib-copy');
  grunt.loadNpmTasks('grunt-mkdir');
  grunt.registerTask('default', ['clean', 'mkdir', 'copy', 'responsive_images']);

};
