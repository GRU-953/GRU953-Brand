// SPDX-License-Identifier: Apache-2.0
// Copyright 2026 Aninda Sundar Howlader (GRU953)
/*
 * svgo configuration for the GRU953 marks.
 *
 * cleanupIds is OFF and must stay off. Every mark carries aria-labelledby="lt ld" on its
 * root, pointing at its own <title> and <desc>. svgo renames those ids to save a few bytes
 * but does not rewrite the attribute that references them, so the accessible name resolves
 * to nothing and the mark becomes an unlabelled graphic. Six lockups shipped that way once.
 *
 * removeViewBox is OFF because the marks must scale to any size.
 * removeTitle and removeDesc are OFF for the same reason as cleanupIds: they ARE the
 * accessible name and description.
 *
 * This file is passed with --config. The older `--disable=` flag is not supported by this
 * version of svgo and fails the whole run, which is how the ids came to be renamed in the
 * first place — the flag was being silently rejected.
 */
export default {
  multipass: true,
  floatPrecision: 2,
  plugins: [
    {
      name: 'preset-default',
      params: {
        overrides: {
          cleanupIds: false,
          removeUnknownsAndDefaults: false,
          inlineStyles: false,
          minifyStyles: false,
          removeUselessDefs: false,
        },
      },
    },
  ],
};
