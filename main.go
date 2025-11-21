package main

import (
	"gioui.org/app"
	"gioui.org/font/gofont"
	"gioui.org/io/event"
	"gioui.org/layout"
	"gioui.org/op"
	"gioui.org/widget/material"
)

func main() {
	go func() {
		w := app.NewWindow()
		th := material.NewTheme(gofont.Collection())
		var ops op.Ops
		for e := range w.Events() {
			switch e := e.(type) {
			case app.DestroyEvent:
				return
			case app.FrameEvent:
				gtx := layout.NewContext(&ops, e)
				material.H1(th, "Hello, Gio!").Layout(gtx)
				e.Frame(gtx.Ops)
			}
		}
	}()
	app.Main()
}
