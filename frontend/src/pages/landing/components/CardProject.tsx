import { cn } from "@/lib/utils"

type Project = {
    title: string
    description: string
    src: string
}

interface CardProjectProps extends React.HTMLAttributes<HTMLDivElement> {
  project: Project
  aspectRatio?: "portrait" | "square"
  width?: number
  height?: number
}

export function CardProject({
    project,
  aspectRatio = "square",
  className,
  ...props
}: CardProjectProps) {
  return (
    <div className={cn("space-y-3", className)} {...props}>
          <div className="overflow-hidden rounded-md">
            <img
              src={project.src}
              alt={project.title}
              className={cn(
                "h-auto w-auto object-cover transition-all hover:scale-105",
                aspectRatio === "portrait" ? "aspect-[3/4]" : "aspect-square"
              )}
            />
          </div>
      <div className="space-y-1 text-sm">
        <h2 className="font-medium leading-none">{project.title}</h2>
        <p className="text-xs text-muted-foreground">{project.description}</p>
      </div>
    </div>
  )
}