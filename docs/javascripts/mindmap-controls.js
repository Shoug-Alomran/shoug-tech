(function () {
    'use strict';

    function mouseEvent(type, point, target) {
        var event = new MouseEvent(type, {
            bubbles: true,
            cancelable: true,
            clientX: point.x,
            clientY: point.y,
            button: 0,
            buttons: type === 'mouseup' ? 0 : 1,
            view: window
        });
        (target || window).dispatchEvent(event);
    }

    function wheelEvent(point, deltaY, target) {
        target.dispatchEvent(new WheelEvent('wheel', {
            bubbles: true,
            cancelable: true,
            clientX: point.x,
            clientY: point.y,
            deltaY: deltaY,
            ctrlKey: true,
            deltaMode: WheelEvent.DOM_DELTA_PIXEL
        }));
    }

    function midpoint(a, b) {
        return { x: (a.clientX + b.clientX) / 2, y: (a.clientY + b.clientY) / 2 };
    }

    function distance(a, b) {
        return Math.hypot(a.clientX - b.clientX, a.clientY - b.clientY);
    }

    function install(viewport) {
        if (!viewport || viewport.dataset.gestureControls === 'true') return;
        viewport.dataset.gestureControls = 'true';
        viewport.style.touchAction = 'none';
        viewport.style.overscrollBehavior = 'contain';

        var touches = new Map();
        var dragging = false;
        var dragPoint = null;
        var pinchDistance = 0;

        viewport.addEventListener('wheel', function (event) {
            if (event.__mindmapSynthetic || event.ctrlKey || event.metaKey) return;
            event.preventDefault();
            event.stopImmediatePropagation();

            var rect = viewport.getBoundingClientRect();
            var start = {
                x: event.clientX || rect.left + rect.width / 2,
                y: event.clientY || rect.top + rect.height / 2
            };
            mouseEvent('mousedown', start, viewport);
            mouseEvent('mousemove', {
                x: start.x - event.deltaX,
                y: start.y - event.deltaY
            }, window);
            mouseEvent('mouseup', start, window);
        }, { passive: false, capture: true });

        viewport.addEventListener('pointerdown', function (event) {
            if (event.pointerType === 'mouse' || event.target.closest('.node, button, input, a, #panel')) return;
            event.preventDefault();
            viewport.setPointerCapture(event.pointerId);
            touches.set(event.pointerId, event);

            if (touches.size === 1) {
                dragPoint = { x: event.clientX, y: event.clientY };
                dragging = true;
                mouseEvent('mousedown', dragPoint, viewport);
            } else if (touches.size === 2) {
                if (dragging) mouseEvent('mouseup', dragPoint, window);
                dragging = false;
                var pair = Array.from(touches.values());
                pinchDistance = distance(pair[0], pair[1]);
            }
        }, { passive: false });

        viewport.addEventListener('pointermove', function (event) {
            if (!touches.has(event.pointerId)) return;
            event.preventDefault();
            touches.set(event.pointerId, event);

            if (touches.size === 1 && dragging) {
                dragPoint = { x: event.clientX, y: event.clientY };
                mouseEvent('mousemove', dragPoint, window);
            } else if (touches.size === 2) {
                var pair = Array.from(touches.values());
                var nextDistance = distance(pair[0], pair[1]);
                var delta = (pinchDistance - nextDistance) * 2.5;
                if (Math.abs(delta) > 0.5) {
                    var synthetic = new WheelEvent('wheel', {
                        bubbles: true,
                        cancelable: true,
                        clientX: midpoint(pair[0], pair[1]).x,
                        clientY: midpoint(pair[0], pair[1]).y,
                        deltaY: delta,
                        ctrlKey: true
                    });
                    Object.defineProperty(synthetic, '__mindmapSynthetic', { value: true });
                    viewport.dispatchEvent(synthetic);
                    pinchDistance = nextDistance;
                }
            }
        }, { passive: false });

        function endPointer(event) {
            if (!touches.has(event.pointerId)) return;
            event.preventDefault();
            touches.delete(event.pointerId);
            if (dragging) mouseEvent('mouseup', dragPoint || { x: event.clientX, y: event.clientY }, window);
            dragging = false;
            pinchDistance = 0;

            if (touches.size === 1) {
                var remaining = Array.from(touches.values())[0];
                dragPoint = { x: remaining.clientX, y: remaining.clientY };
                dragging = true;
                mouseEvent('mousedown', dragPoint, viewport);
            }
        }

        viewport.addEventListener('pointerup', endPointer, { passive: false });
        viewport.addEventListener('pointercancel', endPointer, { passive: false });
    }

    function findViewports() {
        var selectors = ['#cw', '#viewport', '#canvas-wrap', '#mindmap-wrap', '#mindmap-container', '.mindmap-wrap', '.canvas-wrap', '.map-viewport'];
        var found = [];
        selectors.forEach(function (selector) {
            document.querySelectorAll(selector).forEach(function (node) {
                if (!found.includes(node)) found.push(node);
            });
        });
        return found;
    }

    function boot() {
        findViewports().forEach(install);
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', boot);
    } else {
        boot();
    }
}());
