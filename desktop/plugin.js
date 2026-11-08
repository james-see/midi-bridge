/**
 * MIDI Bridge desktop plugin — reference + monitor pane.
 */
import { cn, host, useValue } from '@hermes/plugin-sdk'
import { jsx, jsxs } from 'react/jsx-runtime'

const ID = 'midi-bridge'

const DRUMS = [
  ['kick', '🥁'], ['snare', '🪘'], ['hihat', '🎩'],
  ['crash', '💥'], ['ride', '🛴'], ['cowbell', '🔔'],
  ['clap', '👏'], ['low_tom', '🥁'], ['high_tom', '🥁'],
]

const NOTES = [
  ['C3', 48], ['D3', 50], ['E3', 52], ['F3', 53],
  ['G3', 55], ['A3', 57], ['B3', 59],
  ['C4', 60], ['D4', 62], ['E4', 64], ['F4', 65], ['G4', 67],
]

const RECIPES = [
  ['trap-beat', 'Trap', '140-150', 'Dark, 808s, fast hats'],
  ['rap-boom-bap', 'Boom Bap', '88-95', '90s, punchy, dry'],
  ['house-beat', 'House', '124-130', '4-on-floor, dance'],
  ['kanye-style', 'Kanye', '138-142', 'Heavy, 808 tail'],
  ['bach-melody', 'Bach', '60-80', 'Counterpoint, arpeggios'],
  ['mozart-mode', 'Mozart', '100-120', 'Elegant, alberti bass'],
]

function MonitorPane() {
  const [tab, setTab] = useValue(host.state.midiTab ?? 'drums')

  var content = null

  if (tab === 'drums') {
    var items = []
    for (var i = 0; i < DRUMS.length; i++) {
      var d = DRUMS[i]
      items.push(jsxs('div', {
        key: d[0],
        className: 'flex items-center gap-2 py-1',
        children: [
          jsx('span', { className: 'text-base', children: d[1] }),
          jsx('span', { className: 'font-mono text-xs', children: d[0] }),
        ]
      }))
    }
    content = jsxs('div', {
      className: 'flex flex-col gap-2',
      children: [
        jsx('div', { className: 'text-xs text-(--ui-text-quaternary) mb-1', children: 'GM Drum Map (channel 10)' }),
        jsx('div', { children: items })
      ]
    })
  } else if (tab === 'notes') {
    var noteItems = []
    for (var i = 0; i < NOTES.length; i++) {
      var n = NOTES[i]
      noteItems.push(jsxs('div', {
        key: n[0],
        className: 'flex items-center gap-2 py-0.5',
        children: [
          jsx('span', { className: 'font-mono text-xs w-8', children: String(n[1]) }),
          jsx('span', { className: 'text-xs', children: n[0] }),
        ]
      }))
    }
    content = jsxs('div', {
      className: 'flex flex-col gap-1',
      children: [
        jsx('div', { className: 'text-xs text-(--ui-text-quaternary) mb-1', children: 'Note → MIDI Number' }),
        jsx('div', { children: noteItems })
      ]
    })
  } else if (tab === 'recipes') {
    var recipeItems = []
    for (var i = 0; i < RECIPES.length; i++) {
      var r = RECIPES[i]
      recipeItems.push(jsxs('div', {
        key: r[0],
        className: 'flex flex-col gap-0.5 py-1.5 px-2 rounded-md border border-(--ui-stroke-secondary)',
        children: [
          jsxs('div', {
            className: 'flex items-center justify-between',
            children: [
              jsx('span', { className: 'font-medium', children: r[1] }),
              jsx('span', { className: 'text-xs text-(--ui-text-tertiary)', children: r[2] + ' BPM' }),
            ]
          }),
          jsx('span', { className: 'text-xs text-(--ui-text-quaternary)', children: r[3] }),
        ]
      }))
    }
    content = jsxs('div', {
      className: 'flex flex-col gap-1.5',
      children: [
        jsx('div', { className: 'text-xs text-(--ui-text-quaternary) mb-1', children: 'Genre Recipes' }),
        jsx('div', { children: recipeItems })
      ]
    })
  }

  return jsxs('div', {
    className: 'flex h-full flex-col gap-2 p-3 text-sm overflow-hidden',
    children: [
      jsx('div', {
        className: 'font-medium text-(--ui-text-secondary)',
        children: 'MIDI Bridge'
      }),
      // Tabs
      jsxs('div', {
        className: 'flex gap-1 border-b border-(--ui-stroke-secondary) mb-2',
        children: [
          jsx('button', {
            className: cn('px-2 py-1 text-xs rounded-t', tab === 'drums' ? 'bg-(--ui-bg-secondary) text-foreground' : 'text-(--ui-text-tertiary)'),
            onClick: () => setTab('drums'),
            children: 'Drums'
          }),
          jsx('button', {
            className: cn('px-2 py-1 text-xs rounded-t', tab === 'notes' ? 'bg-(--ui-bg-secondary) text-foreground' : 'text-(--ui-text-tertiary)'),
            onClick: () => setTab('notes'),
            children: 'Notes'
          }),
          jsx('button', {
            className: cn('px-2 py-1 text-xs rounded-t', tab === 'recipes' ? 'bg-(--ui-bg-secondary) text-foreground' : 'text-(--ui-text-tertiary)'),
            onClick: () => setTab('recipes'),
            children: 'Recipes'
          }),
        ]
      }),
      // Content
      jsx('div', { className: 'flex-1 overflow-y-auto', children: content }),
    ]
  })
}

export default {
  id: ID,
  name: 'MIDI Bridge',
  defaultEnabled: false,
  register(ctx) {
    ctx.register({
      id: 'monitor',
      area: 'panes',
      title: 'MIDI Monitor',
      data: {
        placement: 'bottom',
        dock: { pane: 'workspace', pos: 'bottom' },
        height: '220px',
      },
      render: () => jsx(MonitorPane, {})
    })
  }
}
