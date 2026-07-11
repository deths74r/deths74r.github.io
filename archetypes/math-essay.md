---
title: "{{ replace .File.ContentBaseName "-" " " | title }}"
subtitle: ""
date: {{ now.Format "2006-01-02" }}
description: ""
tags: []
toc: true
math: true
draft: true
---

<!-- Math essay. `math: true` loads the KaTeX renderer on this page only.
     Inline math: \( ... \)    Display math: $$ ... $$    (see PUBLISHING.md) -->

Open with the question, then the mechanism.

## The setup

Introduce the quantities. For example, an inline rate law: \( v = k[A][B] \).

## The derivation

A display equation:

$$
\frac{d[P]}{dt} = k \, [A][B]
$$

Explain each term and what follows from it.

## Notes

[^1]: Source or note.
