(function () {
  "use strict";

  var storageKey = "shoug-palette";
  var root = document.documentElement;
  var palettes = {
    original: { accent: "#b829ea", bright: "#c940f5", cyber: "#ff2a4b" },
    ocean: { accent: "#3698ff", bright: "#63c9ff", cyber: "#42e8d4" },
    forest: { accent: "#38bf78", bright: "#79ed9e", cyber: "#c9f04b" },
    ember: { accent: "#ff7a32", bright: "#ffad58", cyber: "#ff426e" },
    solar: { accent: "#d9a900", bright: "#ffdc55", cyber: "#ff7b22" },
  };
  var declarations = [];
  var svgColors = [];
  var declarationMap = new WeakMap();
  var svgColorMap = new WeakMap();
  var svgColorAttributes = ["fill", "stroke", "stop-color", "flood-color"];

  if (window.location.pathname.indexOf("/academics/cybersecurity/") === 0) {
    root.setAttribute("data-site-track", "cyber");
  }

  var COLOR_TOKEN = /#[\da-f]{3,8}\b|rgba?\([^)]*\)|hsla?\([^)]*\)/gi;

  function colorToHsl(red, green, blue) {
    red /= 255;
    green /= 255;
    blue /= 255;
    var max = Math.max(red, green, blue);
    var min = Math.min(red, green, blue);
    var delta = max - min;
    var hue = 0;
    var saturation = 0;
    var lightness = (max + min) / 2;

    if (delta) {
      saturation = delta / (1 - Math.abs(2 * lightness - 1));
      switch (max) {
        case red:
          hue = ((green - blue) / delta) % 6;
          break;
        case green:
          hue = (blue - red) / delta + 2;
          break;
        default:
          hue = (red - green) / delta + 4;
      }
      hue *= 60;
      if (hue < 0) hue += 360;
    }

    return { hue: hue, saturation: saturation, lightness: lightness };
  }

  function hslToRgb(hue, saturation, lightness) {
    var chroma = (1 - Math.abs(2 * lightness - 1)) * saturation;
    var section = hue / 60;
    var secondary = chroma * (1 - Math.abs((section % 2) - 1));
    var red = 0;
    var green = 0;
    var blue = 0;

    if (section < 1) [red, green, blue] = [chroma, secondary, 0];
    else if (section < 2) [red, green, blue] = [secondary, chroma, 0];
    else if (section < 3) [red, green, blue] = [0, chroma, secondary];
    else if (section < 4) [red, green, blue] = [0, secondary, chroma];
    else if (section < 5) [red, green, blue] = [secondary, 0, chroma];
    else [red, green, blue] = [chroma, 0, secondary];

    var offset = lightness - chroma / 2;
    return [red, green, blue].map(function (value) {
      return Math.round((value + offset) * 255);
    });
  }

  function parseColor(value) {
    var hex = value.match(/^#([\da-f]{3}|[\da-f]{4}|[\da-f]{6}|[\da-f]{8})$/i);
    if (hex) {
      var raw = hex[1];
      if (raw.length < 5)
        raw = raw
          .split("")
          .map(function (part) {
            return part + part;
          })
          .join("");
      var hasAlpha = raw.length === 8;
      return {
        rgb: [0, 2, 4].map(function (index) {
          return parseInt(raw.slice(index, index + 2), 16);
        }),
        alpha: hasAlpha ? parseInt(raw.slice(6, 8), 16) / 255 : null,
        format: hasAlpha ? "hex-alpha" : "hex",
      };
    }

    var hsl = value.match(
      /^hsla?\(\s*([\d.]+)(?:deg)?\s*[, ]\s*([\d.]+)%\s*[, ]\s*([\d.]+)%(?:\s*[,/]\s*([\d.]+%?))?\s*\)$/i,
    );
    if (hsl) {
      var hslAlpha =
        hsl[4] == null
          ? null
          : hsl[4].indexOf("%") > -1
            ? parseFloat(hsl[4]) / 100
            : parseFloat(hsl[4]);
      return {
        rgb: hslToRgb(
          parseFloat(hsl[1]) % 360,
          parseFloat(hsl[2]) / 100,
          parseFloat(hsl[3]) / 100,
        ),
        alpha: hslAlpha,
        format: hslAlpha == null ? "rgb" : "rgba",
      };
    }

    var rgb = value.match(
      /^rgba?\(\s*([\d.]+)\s*[, ]\s*([\d.]+)\s*[, ]\s*([\d.]+)(?:\s*[,/]\s*([\d.]+%?))?\s*\)$/i,
    );
    if (!rgb) return null;
    var alpha =
      rgb[4] == null
        ? null
        : rgb[4].indexOf("%") > -1
          ? parseFloat(rgb[4]) / 100
          : parseFloat(rgb[4]);
    return {
      rgb: [parseFloat(rgb[1]), parseFloat(rgb[2]), parseFloat(rgb[3])],
      alpha: alpha,
      format:
        value.slice(0, 4).toLowerCase() === "rgba" || alpha != null
          ? "rgba"
          : "rgb",
    };
  }

  function luminance(rgb) {
    var channels = rgb.map(function (value) {
      value /= 255;
      return value <= 0.03928
        ? value / 12.92
        : Math.pow((value + 0.055) / 1.055, 2.4);
    });
    return 0.2126 * channels[0] + 0.7152 * channels[1] + 0.0722 * channels[2];
  }

  // The brightest a colored foreground may be on a light page: about 4.5:1
  // against white and the site's pale tinted panels.
  var LIGHT_TEXT_MAX_LUMINANCE = 0.14;
  // Paler than this is a tinted surface held in a CSS variable, never text.
  var PALE_SURFACE_LUMINANCE = 0.55;

  // Lowers lightness until the hue is no brighter than the limit, so a swap from
  // red or purple to cyan or yellow can't wash out what sits on or under it.
  function darkenToLuminance(hue, saturation, lightness, limit) {
    if (luminance(hslToRgb(hue, saturation, lightness)) <= limit)
      return lightness;
    var low = 0;
    var high = lightness;
    for (var i = 0; i < 16; i += 1) {
      var middle = (low + high) / 2;
      if (luminance(hslToRgb(hue, saturation, middle)) > limit) high = middle;
      else low = middle;
    }
    return low;
  }

  // Very dim grays the pages use for text on dark backgrounds (under 3:1).
  var DIM_TEXT_ON_DARK = {
    "77,58,64": [168, 154, 160],
    "90,79,110": [167, 157, 184],
    "74,66,88": [167, 157, 184],
    "111,98,125": [167, 157, 184],
  };

  // Course pages were written with their own colors, mostly blue. The theme has
  // to reach those too, but green and amber often carry meaning (correct answer,
  // "asked on a past exam"), so they only count when they lead the page.
  var isCoursePage = window.location.pathname.indexOf("/academics/") === 0;
  var SITE_CHROME_SHEET =
    /\/styles\/(site-shell|light-mode|mobile-fixes|a11y|cyber-track)/;
  var BRAND_MIN_SATURATION = 0.35;
  var BRAND_LEAD_SHARE = 0.5;
  var brandFamilies = null;

  function hueFamily(hue) {
    if (hue >= 245 && hue <= 325) return "purple";
    if (hue >= 335 || hue <= 15) return "red";
    if (hue >= 170 && hue < 245) return "blue";
    if (hue >= 75 && hue < 170) return "green";
    if (hue > 15 && hue < 75) return "amber";
    return "";
  }

  function tallyValue(value, counts) {
    (value.match(COLOR_TOKEN) || []).forEach(function (token) {
      var color = parseColor(token);
      if (!color) return;
      var hsl = colorToHsl(color.rgb[0], color.rgb[1], color.rgb[2]);
      if (hsl.saturation < 0.18 || hsl.lightness < 0.06 || hsl.lightness > 0.97)
        return;
      var family = hueFamily(hsl.hue);
      if (family) counts[family] = (counts[family] || 0) + 1;
    });
  }

  function tallyRules(rules, counts) {
    if (!rules) return;
    for (var i = 0; i < rules.length; i += 1) {
      var rule = rules[i];
      if (rule.style) {
        for (var j = 0; j < rule.style.length; j += 1) {
          tallyValue(rule.style.getPropertyValue(rule.style[j]), counts);
        }
      }
      if (rule.cssRules) tallyRules(rule.cssRules, counts);
    }
  }

  // Runs before anything is recolored, because it needs the page's own values.
  function detectBrandFamilies() {
    if (brandFamilies || !isCoursePage) return;
    var counts = {};
    Array.prototype.forEach.call(document.styleSheets, function (sheet) {
      if (sheet.href && SITE_CHROME_SHEET.test(sheet.href)) return;
      try {
        tallyRules(sheet.cssRules, counts);
      } catch (error) {}
    });
    var total = Object.keys(counts).reduce(function (sum, key) {
      return sum + counts[key];
    }, 0);
    if (!total) return;
    var found = {};
    // A mind map's colors only mark branch depth, so all of them follow the theme.
    if (/mind-?map/i.test(window.location.pathname)) {
      found.blue = found.green = found.amber = true;
    } else if (
      ((counts.purple || 0) + (counts.red || 0)) / total <
      BRAND_LEAD_SHARE
    ) {
      found.blue = true;
      ["green", "amber"].forEach(function (family) {
        if ((counts[family] || 0) / total >= BRAND_LEAD_SHARE)
          found[family] = true;
      });
    }
    brandFamilies = found;
  }

  function propertyKind(property) {
    if (property.indexOf("background") === 0) return "background";
    return /border|outline|line|shadow/.test(property) ? "decoration" : "text";
  }

  function writeColor(rgb, color) {
    if (color.format === "hex" || color.format === "hex-alpha") {
      var hex = rgb
        .map(function (part) {
          return part.toString(16).padStart(2, "0");
        })
        .join("");
      if (color.format === "hex-alpha")
        hex += Math.round(color.alpha * 255)
          .toString(16)
          .padStart(2, "0");
      return "#" + hex;
    }
    if (color.alpha == null) return "rgb(" + rgb.join(", ") + ")";
    return "rgba(" + rgb.join(", ") + ", " + color.alpha + ")";
  }

  function formatColor(color, palette, kind) {
    if (kind === "text" && !palette.light && color.alpha == null) {
      var lifted = DIM_TEXT_ON_DARK[color.rgb.join(",")];
      if (lifted) return writeColor(lifted, color);
    }
    var isBackground = kind === "background";
    var hsl = colorToHsl(color.rgb[0], color.rgb[1], color.rgb[2]);
    var hue = hsl.hue;
    var targetHue = null;

    if (hsl.saturation < 0.18) return null;
    var family = hueFamily(hue);
    if (family === "purple") targetHue = palette.accentHue;
    else if (family === "red") targetHue = palette.cyberHue;
    else if (
      brandFamilies &&
      brandFamilies[family] &&
      hsl.saturation >= BRAND_MIN_SATURATION
    )
      targetHue = palette.brandHue;
    else return null;
    if (targetHue == null) {
      // The original palette keeps its hues; only light-page text needs darkening.
      if (isBackground || !palette.light) return null;
      targetHue = hue;
    }

    var lightness = hsl.lightness;
    var originalLuminance = luminance(color.rgb);
    var solid = color.alpha == null || color.alpha >= 0.35;
    if (isBackground) {
      if (solid)
        lightness = darkenToLuminance(
          targetHue,
          hsl.saturation,
          lightness,
          originalLuminance,
        );
    } else if (palette.light && originalLuminance < PALE_SURFACE_LUMINANCE) {
      lightness = darkenToLuminance(
        targetHue,
        hsl.saturation,
        lightness,
        Math.min(originalLuminance, LIGHT_TEXT_MAX_LUMINANCE),
      );
    }
    return writeColor(hslToRgb(targetHue, hsl.saturation, lightness), color);
  }

  function recolorValue(value, palette, kind) {
    return value.replace(COLOR_TOKEN, function (token) {
      var color = parseColor(token);
      return color
        ? formatColor(color, palette, kind || "text") || token
        : token;
    });
  }

  function trackStyle(style, palette) {
    if (!style || !style.length) return;
    var known = declarationMap.get(style);
    if (!palette && !known) return;
    if (!known) {
      known = new Map();
      declarationMap.set(style, known);
    }

    for (var i = 0; i < style.length; i += 1) {
      var property = style[i];
      var current = style.getPropertyValue(property);
      var record = known.get(property);
      if (!record) {
        if (
          !palette ||
          recolorValue(current, palette, propertyKind(property)) === current
        )
          continue;
        record = {
          style: style,
          property: property,
          original: current,
          priority: style.getPropertyPriority(property),
          applied: current,
        };
        known.set(property, record);
        declarations.push(record);
      } else if (record.applied !== current) {
        record.original = current;
        record.priority = style.getPropertyPriority(property);
        record.applied = current;
      }
      if (palette) applyDeclaration(record, palette);
    }
  }

  function trackSvgColors(element, palette) {
    var known = svgColorMap.get(element);
    if (!palette && !known) return;
    if (!known) {
      known = new Map();
      svgColorMap.set(element, known);
    }

    svgColorAttributes.forEach(function (attribute) {
      if (!element.hasAttribute(attribute)) return;
      var current = element.getAttribute(attribute);
      var record = known.get(attribute);
      if (!record) {
        if (!palette || recolorValue(current, palette) === current) return;
        record = {
          element: element,
          attribute: attribute,
          original: current,
          applied: current,
        };
        known.set(attribute, record);
        svgColors.push(record);
      } else if (record.applied !== current) {
        record.original = current;
        record.applied = current;
      }
      applySvgColor(record, palette);
    });
  }

  function applySvgColor(record, palette) {
    var next = palette
      ? recolorValue(record.original, palette)
      : record.original;
    if (record.element.getAttribute(record.attribute) !== next) {
      record.element.setAttribute(record.attribute, next);
    }
    record.applied = next;
  }

  function applyDeclaration(record, palette) {
    var next = palette
      ? recolorValue(record.original, palette, propertyKind(record.property))
      : record.original;
    if (record.style.getPropertyValue(record.property) !== next) {
      record.style.setProperty(record.property, next, record.priority);
    }
    record.applied = next;
  }

  function isPaletteRule(rule) {
    return (
      rule.selectorText && rule.selectorText.indexOf(".shoug-palette-") !== -1
    );
  }

  function scanRules(rules, palette) {
    if (!rules) return;
    for (var i = 0; i < rules.length; i += 1) {
      var rule = rules[i];
      if (rule.style && !isPaletteRule(rule)) trackStyle(rule.style, palette);
      if (rule.cssRules) scanRules(rule.cssRules, palette);
    }
  }

  function scanNode(node, palette) {
    if (!node || node.nodeType !== 1) return;
    if (node.matches("[style]")) trackStyle(node.style, palette);
    if (
      svgColorAttributes.some(function (attribute) {
        return node.hasAttribute(attribute);
      })
    )
      trackSvgColors(node, palette);
    if (node.matches("style")) {
      var sheet = node.sheet;
      if (sheet) {
        try {
          scanRules(sheet.cssRules, palette);
        } catch (error) {}
      }
    }
    node.querySelectorAll("[style]").forEach(function (element) {
      trackStyle(element.style, palette);
    });
    node
      .querySelectorAll("[fill], [stroke], [stop-color], [flood-color]")
      .forEach(function (element) {
        trackSvgColors(element, palette);
      });
    node.querySelectorAll("style").forEach(function (styleElement) {
      if (!styleElement.sheet) return;
      try {
        scanRules(styleElement.sheet.cssRules, palette);
      } catch (error) {}
    });
  }

  function scanDocument(palette) {
    Array.prototype.forEach.call(document.styleSheets, function (sheet) {
      try {
        scanRules(sheet.cssRules, palette);
      } catch (error) {}
    });
    document.querySelectorAll("[style]").forEach(function (element) {
      trackStyle(element.style, palette);
    });
    document
      .querySelectorAll("[fill], [stroke], [stop-color], [flood-color]")
      .forEach(function (element) {
        trackSvgColors(element, palette);
      });
  }

  function themeHue(hex) {
    var color = parseColor(hex);
    return colorToHsl(color.rgb[0], color.rgb[1], color.rgb[2]).hue;
  }

  function pageIsLight() {
    if (document.body && document.body.classList.contains("shoug-light-mode"))
      return true;
    var theme = root.getAttribute("data-theme");
    if (theme) return theme === "light";
    var surfaces = [document.body, root];
    for (var i = 0; i < surfaces.length; i += 1) {
      if (!surfaces[i]) continue;
      var color = parseColor(getComputedStyle(surfaces[i]).backgroundColor);
      if (color && color.alpha !== 0) return luminance(color.rgb) > 0.5;
    }
    return false;
  }

  var lightPage = false;

  function currentPalette() {
    var selected = root.getAttribute("data-site-palette") || "original";
    var colors = palettes[selected] || palettes.original;
    var brandHue =
      root.getAttribute("data-site-track") === "cyber"
        ? themeHue(colors.cyber)
        : themeHue(colors.accent);
    if (selected === "original")
      return {
        accentHue: null,
        cyberHue: null,
        brandHue: brandHue,
        light: lightPage,
      };
    return {
      brandHue: brandHue,
      accentHue:
        root.getAttribute("data-site-track") === "cyber"
          ? themeHue(colors.cyber)
          : themeHue(colors.accent),
      cyberHue: themeHue(colors.cyber),
      light: lightPage,
    };
  }

  // Theme colors used directly as text need the same limit on a light page.
  function readableHex(hex) {
    if (!lightPage) return hex;
    var hsl = colorToHsl.apply(null, parseColor(hex).rgb);
    var lightness = darkenToLuminance(
      hsl.hue,
      hsl.saturation,
      hsl.lightness,
      LIGHT_TEXT_MAX_LUMINANCE,
    );
    return (
      "#" +
      hslToRgb(hsl.hue, hsl.saturation, lightness)
        .map(function (part) {
          return part.toString(16).padStart(2, "0");
        })
        .join("")
    );
  }

  function setTheme(value) {
    var selected = palettes[value] ? value : "original";
    var colors = palettes[selected];
    lightPage = pageIsLight();
    detectBrandFamilies();
    root.setAttribute("data-site-palette", selected);
    var palette = currentPalette();
    var accent = readableHex(colors.accent);
    var cyber = readableHex(colors.cyber);

    root.style.setProperty("--sg-accent", accent, "important");
    root.style.setProperty(
      "--sg-accent-bright",
      readableHex(colors.bright),
      "important",
    );
    root.style.setProperty("--sg-cyber", cyber, "important");
    root.style.setProperty(
      "--sg-accent-rgb",
      hexToRgbString(accent),
      "important",
    );
    root.style.setProperty(
      "--sg-cyber-rgb",
      hexToRgbString(cyber),
      "important",
    );
    scanDocument(palette);
    declarations.forEach(function (record) {
      applyDeclaration(record, palette);
    });
    svgColors.forEach(function (record) {
      applySvgColor(record, palette);
    });

    document
      .querySelectorAll("[data-site-palette-option]")
      .forEach(function (button) {
        button.setAttribute(
          "aria-pressed",
          button.getAttribute("data-site-palette-option") === selected
            ? "true"
            : "false",
        );
      });
    document
      .querySelectorAll("[data-site-palette-trigger]")
      .forEach(function (button) {
        button.setAttribute(
          "aria-label",
          "Color theme: " + selected.replace("-", " "),
        );
      });
    return selected;
  }

  function hexToRgbString(hex) {
    var color = parseColor(hex);
    return color.rgb.join(", ");
  }

  var builtControl = null;
  var embedded = true;
  try {
    embedded = window.self !== window.top;
  } catch (error) {}

  // Header on normal pages, the account bar on app pages, else a floating button.
  function placePicker() {
    if (!builtControl) return;
    var host =
      document.getElementById("shoug-app-nav") ||
      document.querySelector(".shoug-header-actions");
    if (!host) {
      builtControl.setAttribute("data-site-palette-floating", "");
      if (builtControl.parentNode !== document.body)
        document.body.appendChild(builtControl);
      return;
    }
    builtControl.removeAttribute("data-site-palette-floating");
    if (builtControl.parentNode === host) return;
    var next = host.querySelector(
      ":scope > .shoug-lang-btn, :scope > #shoug-theme-toggle",
    );
    host.insertBefore(builtControl, next);
  }

  function mountFallbackPicker() {
    // Embedded course content follows the page around it, so it needs no picker.
    if (
      embedded ||
      document.querySelector("[data-site-palette-trigger]") ||
      !document.body
    )
      return;

    var control = document.createElement("div");
    control.className = "shoug-palette-control";

    var trigger = document.createElement("button");
    trigger.className = "shoug-palette-trigger";
    trigger.type = "button";
    trigger.setAttribute("aria-expanded", "false");
    trigger.setAttribute("aria-controls", "shoug-palette-menu-floating");
    trigger.setAttribute("aria-label", "Choose website color theme");
    trigger.setAttribute("data-site-palette-trigger", "");

    var preview = document.createElement("span");
    preview.className = "shoug-palette-preview";
    preview.setAttribute("aria-hidden", "true");
    preview.appendChild(document.createElement("i"));
    preview.appendChild(document.createElement("i"));
    trigger.appendChild(preview);

    var triggerLabel = document.createElement("span");
    triggerLabel.textContent = "Theme";
    trigger.appendChild(triggerLabel);

    var menu = document.createElement("div");
    menu.className = "shoug-palette-menu";
    menu.id = "shoug-palette-menu-floating";
    menu.setAttribute("role", "group");
    menu.setAttribute("aria-label", "Website color theme");
    menu.setAttribute("data-site-palette-menu", "");
    menu.hidden = true;

    Object.keys(palettes).forEach(function (name) {
      var option = document.createElement("button");
      option.type = "button";
      option.className = "shoug-palette-option";
      option.setAttribute("data-site-palette-option", name);
      option.setAttribute(
        "aria-pressed",
        name === "original" ? "true" : "false",
      );

      var swatches = document.createElement("span");
      swatches.className = "shoug-palette-swatches";
      swatches.setAttribute("aria-hidden", "true");
      swatches.appendChild(document.createElement("i"));
      swatches.appendChild(document.createElement("i"));
      option.appendChild(swatches);

      var label = document.createElement("span");
      label.textContent =
        name === "original"
          ? "Cyber original"
          : name.charAt(0).toUpperCase() + name.slice(1) + " cyber";
      option.appendChild(label);

      var check = document.createElement("span");
      check.className = "shoug-palette-check";
      check.setAttribute("aria-hidden", "true");
      check.textContent = "✓";
      option.appendChild(check);
      menu.appendChild(option);
    });

    control.appendChild(trigger);
    control.appendChild(menu);
    builtControl = control;
    placePicker();
  }

  function closeMenus() {
    document
      .querySelectorAll("[data-site-palette-menu]")
      .forEach(function (menu) {
        menu.hidden = true;
      });
    document
      .querySelectorAll("[data-site-palette-trigger]")
      .forEach(function (button) {
        button.setAttribute("aria-expanded", "false");
      });
  }

  var saved = "original";
  try {
    saved = localStorage.getItem(storageKey) || "original";
  } catch (error) {}
  mountFallbackPicker();
  setTheme(saved);

  document
    .querySelectorAll("[data-site-palette-trigger]")
    .forEach(function (trigger) {
      trigger.addEventListener("click", function () {
        var menu = trigger.parentElement.querySelector(
          "[data-site-palette-menu]",
        );
        var open = menu && menu.hidden;
        closeMenus();
        if (menu && open) {
          menu.hidden = false;
          trigger.setAttribute("aria-expanded", "true");
          menu.querySelector("[aria-pressed='true']")?.focus();
        }
      });
    });

  document
    .querySelectorAll("[data-site-palette-option]")
    .forEach(function (button) {
      button.addEventListener("click", function () {
        var selected = setTheme(
          button.getAttribute("data-site-palette-option"),
        );
        try {
          localStorage.setItem(storageKey, selected);
        } catch (error) {}
        closeMenus();
        document.querySelector("[data-site-palette-trigger]")?.focus();
      });
    });

  document.addEventListener("click", function (event) {
    if (!event.target.closest(".shoug-palette-control")) closeMenus();
  });
  document.addEventListener("keydown", function (event) {
    if (
      event.key === "Escape" &&
      document.querySelector("[data-site-palette-menu]:not([hidden])")
    ) {
      closeMenus();
      document.querySelector("[data-site-palette-trigger]")?.focus();
    }
  });

  window.addEventListener("storage", function (event) {
    if (event.key === storageKey) setTheme(event.newValue || "original");
  });
  window.addEventListener("load", function () {
    setTheme(root.getAttribute("data-site-palette"));
  });

  function recheckPageMode() {
    if (pageIsLight() !== lightPage)
      setTheme(root.getAttribute("data-site-palette"));
  }

  if (window.MutationObserver) {
    var modeObserver = new MutationObserver(recheckPageMode);
    modeObserver.observe(root, {
      attributes: true,
      attributeFilter: ["class", "data-theme"],
    });
    if (document.body)
      modeObserver.observe(document.body, {
        attributes: true,
        attributeFilter: ["class"],
      });

    new MutationObserver(function (mutations) {
      placePicker();
      var palette = currentPalette();
      mutations.forEach(function (mutation) {
        if (mutation.type === "attributes") scanNode(mutation.target, palette);
        else {
          scanNode(mutation.target, palette);
          mutation.addedNodes.forEach(function (node) {
            scanNode(node, palette);
          });
        }
      });
    }).observe(document.documentElement, {
      attributes: true,
      attributeFilter: ["style", "fill", "stroke", "stop-color", "flood-color"],
      childList: true,
      subtree: true,
    });
  }
})();
